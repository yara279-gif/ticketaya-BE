from django.db import models

class Party(models.Model):
    name = models.CharField(max_length=100)
    performer = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    datetime = models.DateTimeField()
    number_of_tickets = models.IntegerField()
    
    def __str__(self):
        return self.name
