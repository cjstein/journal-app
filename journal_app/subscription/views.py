from django.shortcuts import render
from django.conf import settings
from django.http.response import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import stripe


@login_required
def home(request):
    return render(request, "subscription/home.html")


@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        context = {'publicKey': settings.STRIPE_TEST_PUBLIC_KEY}
        return JsonResponse(context, safe=False)


@csrf_exempt
def create_checkout_session(request):
    if request.method == 'GET':
        domain_url = 'http://localhost:8000/'
        stripe.api_key = settings.STRIPE_TEST_SECRET_KEY
        try:
            checkout_session = stripe.checkout.Session.create(
                client_reference_id=request.user.id if request.user.is_authenticated else None,
                success_url=domain_url + 'subscription/success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'subscription/cancel/',
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
