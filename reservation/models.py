from django.db import models
from match.models import Match
from account.models import User

# Create your models here.


class match_reservation(models.Model):
    match_id = models.ForeignKey(Match, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    tickets_reserved = models.IntegerField()

    date_of_reservation = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    pay_method_choices = (
        ("offline", "cash"),
        ("online", "visa_card"),
    )
    pay_method = models.CharField(
        max_length=30, choices=pay_method_choices, default="offline"
    )
    price = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)


class online_match_payment(models.Model):

    reservation_id = models.ForeignKey(match_reservation, on_delete=models.CASCADE)
    visa_card = models.CharField(max_length=16)
    PAYMENT_STATUS_PENDING = "P"
    PAYMENT_STATUS_COMPLETE = "c"
    PAYMENT_STATUS_FAILD = "F"
    PAYMENT_STATUS_CHOICES = (
        (PAYMENT_STATUS_PENDING, "Pending"),
        (PAYMENT_STATUS_COMPLETE, "Complete"),
        (PAYMENT_STATUS_FAILD, "Failed"),
    )
    payment_status = models.CharField(
        null=True,
        blank=True,
        max_length=1,
        choices=PAYMENT_STATUS_CHOICES,
        default=PAYMENT_STATUS_PENDING,
    )
    REQUIRED_FIELDS = ["match_id", "user_id", "visa_card"]
