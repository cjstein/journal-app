from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import Site
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt

import stripe

from journal_app.journal_mail.models import Mail
from journal_app.subscription.models import StripeCustomer, Subscription
from journal_app.users.models import User


@login_required
def home(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    try:
        customer = StripeCustomer.objects.get(user=request.user)
        if not customer.stripe_customer_id:
            stripe_customer = stripe.Customer.create(
                email=request.user.email,
                description=str(request.user)
            )
            customer.stripe_customer_id = stripe_customer.id
            customer.save()
    except ObjectDoesNotExist:
        stripe_customer = stripe.Customer.create(
            email=request.user.email,
            description=str(request.user),
        )
        customer = StripeCustomer.objects.create(user=request.user, stripe_customer_id=stripe_customer.stripe_id)
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
    product = Subscription.objects.get(uuid=price_uuid)
    try:
        customer = StripeCustomer.objects.get(user=request.user)
        customer_id = customer.stripe_customer_id
        print(customer_id)
        subscription_id = customer.stripe_subscription_id

    except StripeCustomer.DoesNotExist:
        customer_id = None
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
    user = User.objects.get(username=request.user.username)
    customer = StripeCustomer.objects.get(user=user)
    customer.get_subscription_status()
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
        session = event['data']['object']
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400, content=e)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400, content=e)
    if settings.DEBUG:
        try:
            with open(r'Desktop/event_test.txt', 'w') as f:
                f.write(event)
        except:  # noqa E722
            pass
    stripe_customer_id = session.get('customer').strip()
    event_type = event['type'].strip()
    print(f'type:{event_type}::{stripe_customer_id}')
    if event_type == "customer.subscription.updated":
        try:
            stripe_subscription_id = session.get('items').get('data')[0].get('subscription')
            customer = StripeCustomer.objects.get(stripe_customer_id=stripe_customer_id)
            if not customer.stripe_subscription_id:
                customer.stripe_subscription_id = stripe_subscription_id
                customer.save()
            customer.get_subscription_status()
            customer.save()
            print(f'{customer.stripe_customer_id}::{customer.stripe_subscription_id} updated')
        except StripeCustomer.DoesNotExist as e:
            print(stripe_customer_id)
            print(e)
        except Exception as e:
            print(e)
    if event_type == "customer.subscription.created":
        print("creating...")
        try:
            stripe_subscription_id = session.get('subscription').strip()
            print(stripe_subscription_id)
            customer = StripeCustomer.objects.get(stripe_customer_id=stripe_customer_id)
            customer.status = StripeCustomer.Status.ACTIVE
            customer.stripe_subscription_id = stripe_subscription_id
            customer.save()
            customer.get_subscription_status()
            customer.save()
            mail = Mail.objects.create(
                user=customer.user,
                subject="Thanks for subscribing!",
                template_name='subscription_success',
            )
            mail.message()
            print(f'{customer.stripe_customer_id}::{customer.stripe_subscription_id} created')
        except StripeCustomer.DoesNotExist as e:
            print(stripe_customer_id)
            print(e)
        except Exception as e:
            print(e)
    if event_type == "customer.subscription.deleted":
        print('deleting...')
        # Occurs whenever a customer's subscription ends.
        print(stripe_customer_id)
        customer = StripeCustomer.objects.get(stripe_customer_id=stripe_customer_id)
        customer.status = StripeCustomer.Status.CANCELLED
        customer.stripe_subscription_id = None
        customer.subscription_end = None
        customer.subscription_start = None
        customer.product_name = None
        customer.subscription_cache = session.get('items').get('data')[0]
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
