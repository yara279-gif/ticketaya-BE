from django.db import models
from account.models import User


class Party(models.Model):

    name = models.CharField(max_length=100, unique=True)
    performer = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    datetime = models.DateTimeField()
    number_of_tickets = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    description = models.CharField(max_length=1000, null=True)
    image = models.ImageField(upload_to="parties/%y/%m/%d", blank=True, null=True)
    avilable = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Party_user(models.Model):
    party = models.ForeignKey(Party, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)


# -----------------------------(party reservation)-----------------------------

class Party_reservation(models.Model):
    party_id = models.ForeignKey(Party, on_delete=models.CASCADE)
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


class online_party_payment(models.Model):

    reservation_id = models.ForeignKey(Party_reservation, on_delete=models.CASCADE)
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
    REQUIRED_FIELDS = ["party_id", "user_id", "visa_card"]
