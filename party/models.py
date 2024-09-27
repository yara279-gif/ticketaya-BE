from django.db import models
from account.models import User
class Party(models.Model):

    name = models.CharField(max_length=100,unique=True)
    performer = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    datetime = models.DateTimeField()
    number_of_tickets = models.IntegerField()
    price=models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)
    available=models.BooleanField(default=False)
    image = models.ImageField(upload_to='images/%y/%m/%d',default='images/24/9/12/party.jpeg')
    def __str__(self):
        return self.name
class Party_user(models.Model):
    party=models.ForeignKey(Party,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    total=models.DecimalField(max_digits=10,decimal_places=2,default=0)
    card_cvv=models.CharField(max_length=3)
    month=models.CharField(max_length=2)
    year=models.CharField(max_length=2)
    
    