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
    if request.method != 'GET':
        return
    domain_url = Site.objects.get_current().domain
    domain_url = domain_url if domain_url.startswith('http') else fr'https://{domain_url}'
    stripe.api_key = settings.STRIPE_SECRET_KEY
    price_uuid = request.GET.get('price', None)
    product = Subscription.objects.get(uuid = price_uuid)
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
                    'price': product.stripe_price_id,
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
    if event['type'].strip() == 'checkout.session.completed':
        session = event['data']['object']

        # Fetch all the required data from session
        client_reference_id = session.get('client_reference_id')
        stripe_customer_id = session.get('customer')
        stripe_subscription_id = session.get('subscription')

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
        customer.get_subscription_status()
    if event['type'].strip() == "customer.subscription.created" or event['type'].strip() == "customer.subscription.updated":
        if event['type'].strip() == "customer.subscription.created":
            print("creating...")
        else:
            print('updating...')
        # Occurs whenever a customer is signed up for a new plan.
        # Occurs whenever a subscription changes
        # (e.g., switching from one plan to another,
        # or changing the status from trial to active).
        session = event['data']['object']
        stripe_customer_id = session.get('customer').strip()
        try:
            customer = StripeCustomer.objects.get(stripe_customer_id=stripe_customer_id)
            customer.subscription_start = int(session.get('current_period_start'))
            customer.subscription_end = int(session.get('current_period_end'))
            customer.product = session.get('id')
            customer.subscription = Subscription.objects.get(uuid=session.get('metadata')['uuid'])
            customer.status = StripeCustomer.Status.ACTIVE
            customer.save()
        except StripeCustomer.DoesNotExist as e:
            print(stripe_customer_id)
            print(e)
    if event['type'].strip() == "customer.subscription.deleted":
        print('deleting...')
        # Occurs whenever a customer's subscription ends.
        stripe_customer_id = event['data']['object']['customer'].strip()
        print(stripe_customer_id)
        customer = StripeCustomer.objects.get(stripe_customer_id=stripe_customer_id)
        customer.status = StripeCustomer.Status.CANCELLED
        customer.stripe_subscription_id = None
        customer.subscription_end = None
        customer.subscription_start = None
        customer.save()
        # TODO add an email to confirm cancellation
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
