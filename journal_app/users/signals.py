from django.dispatch import receiver

from allauth.account.signals import email_confirmed


@receiver(email_confirmed)
def user_email_confirmed(request, email_address, **kwargs):
    user = email_address.user
    user.email_verified = True
    user.save()
