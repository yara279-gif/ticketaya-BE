from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from . import serializers
from django.contrib.auth import authenticate
from .renderers import userrenderer
from rest_framework_simplejwt.tokens import RefreshToken
from .permissions import IsAuthOrReadOnly
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.exceptions import ValidationError
from .models import match_reservation
from match.models import Match
from match.views import update_match

# Create your views here.

@api_view(["POST"])
def book_match (request,pk):
    
    renderer_classes= [userrenderer]
    permission_classes = [IsAuthenticated]
    try:
        match_id = Match.objects.get(pk=pk)
    except  Match.DoesNotExist:
        return Response({"error": "Match not found"}, status=status.HTTP_404_NOT_FOUND)
    if match_id.avilable == True:

        serializer= serializers.bookmatchserializer(data = request.data)
        
        if  serializer.is_valid():
            serializer.save(user_id = request.user,match_id = match_id)
            x=match_id.no_tickets
            match_id.no_tickets -= serializer.data.get("tickets_reserved")
            if  match_id.no_tickets <0:
                return Response({"error": ["Not enough tickets",f'you can book up to  {x} tickets only!']}, status=status.HTTP_400_BAD_REQUEST)
            if match_id.no_tickets ==0:
                match_id.avilable = False
            match_id.save()
            # serializer.data.get("price")=  match_id.price * serializer.data.get("tickets_reserved")
            price =  match_id.ticket_price * serializer.data.get("tickets_reserved")



            return Response({'msg':['Done!',f'the price is {price}']}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_406_NOT_ACCEPTABLE)
    else:
        return Response({"error": "Match is not available"}, status=status.HTTP_400_BAD_REQUEST)




                   