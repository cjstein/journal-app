import stripe
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import Site
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from journal_app.subscription.models import StripeCustomer, Subscription
from journal_app.journal_mail.models import Mail
from journal_app.users.models import User


@login_required
def home(request):
    customer = StripeCustomer.objects.get(user=request.user)
    subscriptions = Subscription.objects.all()
    context = {
        'user': request.user,
        'customer': customer,
        'subscriptions': subscriptions
    }
    return render(request, 'subscription/home.html', context)


@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        context = {'publicKey': settings.STRIPE_PUBLIC_KEY}
        return JsonResponse(context, safe=False)


@csrf_exempt
def create_checkout_session(request, **kwargs):
    if request.method == 'GET':
        domain_url = Site.objects.get_current().domain
        domain_url = domain_url if domain_url.startswith('http') else fr'https://{domain_url}'
        stripe.api_key = settings.STRIPE_SECRET_KEY
        price = request.GET.get('price', None)
        try:
            customer = StripeCustomer.objects.get(user=request.user)
            customer_id = customer.stripe_customer_id
            subscription_id = customer.stripe_subscription_id
            email = request.user.email

        except StripeCustomer.DoesNotExist:
            customer_id = None
            email = request.user.email
            subscription_id = None

        try:
            checkout_session = stripe.checkout.Session.create(
                customer=customer_id,
                subscription=subscription_id,
                client_reference_id=request.user.id if request.user.is_authenticated else None,
                success_url=domain_url + '/subscription/success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + '/subscription/cancel/',
                payment_method_types=['card'],
                mode='subscription',
                line_items=[
                    {
                        'price': price,
                        'quantity': 1,
                    }
                ]
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})


@login_required
def success(request):
    messages.add_message(request, messages.SUCCESS, "Subscription confirmed")
    # user = User.objects.get(username=request.user.username)
    # customer = StripeCustomer.objects.get(user=user)
    # customer.get_subscription_status()
    return render(request, 'subscription/success.html')


@login_required
def cancel(request):
    messages.add_message(request, messages.ERROR, "Subscription not started successfully")
    return render(request, 'subscription/cancel.html')


@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400, content=e)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400, content=e)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        # Fetch all the required data from session
        client_reference_id = session.get('client_reference_id')
        stripe_customer_id = session.get('customer')
        stripe_subscription_id = session.get('subscription')
        print(client_reference_id)
        print(stripe_customer_id)
        print(stripe_subscription_id)

        # Get the user and create a new StripeCustomer
        user = User.objects.get(id=client_reference_id)
        customer = StripeCustomer.objects.get(
            user=user,
        )
        if not customer.stripe_customer_id:
            customer.stripe_customer_id = stripe_customer_id
        customer.stripe_subscription_id = str(stripe_subscription_id)
        customer.status = StripeCustomer.Status.ACTIVE
        customer.save()
        subject = 'Thanks for subscribing'
        mail = Mail(
            user=user,
            subject=subject,
            header=subject,
            template_name='subscription_success',
            )
        mail.message()
    # if event['type'] in ["customer.subscription.created", "customer.subscription.updated"]:
    #     # Occurs whenever a customer is signed up for a new plan.
    #     # Occurs whenever a subscription changes
    #     # (e.g., switching from one plan to another,
    #     # or changing the status from trial to active).
    #     session = event['data']['object']
    #     stripe_subscription_id = session.get('id')
    #     customer = StripeCustomer.objects.get(stripe_subscription_id=stripe_subscription_id)
    #     customer.subscription_start = session.get('current_period_start')
    #     customer.subscription_end = session.get('current_period_end')
    #     customer.product = session.get('id')
    #     customer.status = StripeCustomer.Status.ACTIVE
    #     customer.save()
    if event['type'] == " customer.subscription.deleted":
        # Occurs whenever a customer's subscription ends.
        stripe_subscription_id = event['data']['object']['id']
        customer = StripeCustomer.objects.get(stripe_subscription_id=stripe_subscription_id)
        customer.status = StripeCustomer.Status.CANCELLED
        customer.save()
    return HttpResponse(status=200)


@csrf_exempt
def create_stripe_portal_session(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    domain_url = Site.objects.get_current().domain
    domain_url = domain_url if domain_url.startswith('http') else fr'https://{domain_url}'
    customer = StripeCustomer.objects.get(user=request.user)
    session = stripe.billing_portal.Session.create(
        customer=customer.stripe_customer_id,
        return_url=f'{domain_url}/subscription/',
    )
    return redirect(session.url)
