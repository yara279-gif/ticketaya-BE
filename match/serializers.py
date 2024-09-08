from rest_framework import serializers
from . models import Match

# class add_match (serializers.ModelSerializer):

#     class Meta :
#         model = Match
#         fields = '__all__'

class match (serializers.ModelSerializer):
    class Meta :
        model = Match
        fields = '__all__'


class search_match (serializers.ModelSerializer):
    class Meta :
        model = Match
        fields = ['name','team1','team2']


