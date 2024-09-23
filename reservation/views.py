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
from .models import match_reservation,online_match_payment
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
    
    
@api_view(["POST"])

def  cancel_reservation (request,pk):
    renderer_classes= [userrenderer]
    permission_classes = [IsAuthenticated]
    try:
        reservation = match_reservation.objects.get(pk=pk)
    except match_reservation.DoesNotExist:
        return Response({"error": "Reservation not found"}, status=status.HTTP_404_NOT_FOUND)
    if reservation.user_id == request.user:
        reservation.delete()
        return Response({"msg": "Reservation cancelled"}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "You are not the owner of this reservation"}, status=status.HTTP_400_BAD_REQUEST)


# @api_view(["POST"])
# def match_payment (request,pk):
#     renderer_classes= [userrenderer]
#     permission_classes = [IsAuthenticated]
#     #get the object from  the database
#     #check if the reservation is valid
#     try:
#         reservation = match_reservation.objects.get(pk=pk)
#     except match_reservation.DoesNotExist:
#         return Response({"error": "Reservation not found"}, status=status.HTTP_404_NOT_ACCEPTABLE)
    
#     #check if the reservation is valid
#     if reservation.user_id == request.user:
#         #check if the payment is valid
#         if reservation.payment_status == "pending":
#             #update the payment status to paid
#             reservation.payment_status = "paid"
#             reservation.save()
#             return Response({"msg": "Payment done"}, status=status.HTTP_200_OK)
#         else:
#             return Response({"error": "Payment is already done"}, status=status.HTTP_400_BAD_REQUEST)
#     else:
#         return Response({"error": "You are not the owner of this reservation"}, status=status.HTTP_400_BAD_REQUEST)
        
@api_view(['POST'])
def  match_payment (request,pk):
    renderer_classes = [userrenderer]
    permission_classes = [IsAuthenticated]
    try:
        reservation_id = match_reservation.objects.get(pk = pk)
        match = reservation_id.match_id
    except match_reservation.DoesNotExist:
        return Response({"error": "You already paid for this match"}, status=status.HTTP_404_NOT_FOUND)

    
    serializer = serializers.matchpaymentserializer(data=request.data)
    if serializer.is_valid():
        serializer.save(reservation_id=reservation_id)  # Saving the reservation in the payment
        reservation_id.delete()
        return Response({"msg": "Payment successful"}, status=status.HTTP_200_OK)
    else:
        match.no_tickets += reservation_id.tickets_reserved
        match.save()
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    


                








    





                   