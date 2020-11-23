import stripe
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import Site
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils.timezone import datetime
from django.views.decorators.csrf import csrf_exempt

from journal_app.subscription.models import StripeCustomer
from journal_app.subscription.utils import get_subscription_status
from journal_app.journal_mail.models import Mail
from journal_app.users.models import User


@login_required
def home(request):
    return render(request, 'subscription/home.html', get_subscription_status(request.user))


@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        context = {'publicKey': settings.STRIPE_PUBLIC_KEY}
        return JsonResponse(context, safe=False)


@csrf_exempt
def create_checkout_session(request):
    if request.method == 'GET':
        domain_url = Site.objects.get_current().domain
        domain_url = domain_url if domain_url.startswith('http') else fr'https://{domain_url}'
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            checkout_session = stripe.checkout.Session.create(
                client_reference_id=request.user.id if request.user.is_authenticated else None,
                success_url=domain_url + '/subscription/success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + '/subscription/cancel/',
                payment_method_types=['card'],
                mode='subscription',
                line_items=[
                    {
                        'price': settings.TEST_STRIPE_PRICE_ID,
                        'quantity': 1,
                    }
                ]
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})


@login_required
def success(request):
    return render(request, 'subscription/success.html')


@login_required
def cancel(request):
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

        # Get the user and create a new StripeCustomer
        user = User.objects.get(id=client_reference_id)
        StripeCustomer.objects.create(
            user=user,
            stripe_customer_id=stripe_customer_id,
            stripe_subscription_id=stripe_subscription_id,
        )
        subject = 'Thanks for subscribing'
        mail = Mail(
            user=user,
            subject=subject,
            header=subject,
            template_name='subscription_success',
            )
        mail.message()

    return HttpResponse(status=200)
