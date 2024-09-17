from django.db import models
from match .models import Match
from account.models import User

# Create your models here.

class match_reservation (models.Model):
    match_id = models.ForeignKey(Match,on_delete = models.CASCADE)
    user_id = models.ForeignKey(User,on_delete = models.CASCADE)
    tickets_reserved = models.IntegerField()
    


    