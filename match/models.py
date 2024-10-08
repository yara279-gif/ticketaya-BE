from django.db import models

# Create your models here.


class Match(models.Model):
    # attributes
    name = models.CharField(max_length=255, unique=True)
    team1 = models.CharField(max_length=255)
    team2 = models.CharField(max_length=255)
    # datetime =  models.DateTimeField(auto_now_add=False,blank=True,null=True)
    date = models.DateField(auto_now_add=False, blank=True, null=True)
    time = models.TimeField(auto_now_add=False, blank=True, null=True)
    stadium = models.CharField(max_length=255)
    no_tickets = models.IntegerField(default=0)
    ticket_price = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    description = models.TextField(blank=True, null=True)
    avilable = models.BooleanField(default=True)
    image = models.ImageField(upload_to="matches/%y/%m/%d", blank=True, null=True)

    def __str__(self):
        return self.name + " - " + self.team1 + " vs " + self.team2
