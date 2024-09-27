

from wsgiref.simple_server import ServerHandler

from rest_framework import serializers


from .models import Party,Party_user

class PartySerializer(serializers.ModelSerializer):
    class Meta:
        model = Party
        fields = ["id", "name", "performer", "location", "datetime", "number_of_tickets","price","available"]
        
class User_partySerializer(serializers.ModelSerializer):
    class Meta:
        model=Party_user
        fields=['party','user','total','card_cvv','month','year']

class show(serializers.Serializer):
    username=serializers.CharField( )
    name=serializers.CharField( )
    total=serializers.DecimalField(max_digits=10,decimal_places=2)
    
