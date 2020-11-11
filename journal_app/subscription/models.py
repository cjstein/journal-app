from django.db import models
from journal_app.users.models import User


class StripeCustomer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=255)
    stripe_subscription_id = models.CharField(max_length=255)

    def __str__(self):
        return str(self.user)
