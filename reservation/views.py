from rest_framework.permissions import IsAuthenticated
from rest_framework import status
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
from .models import match_reservation, online_match_payment
from match.models import Match
from django.template.loader import render_to_string
from account.utils import Util
from match.views import update_match
from account.models import User

# Create your views here.


@api_view(["POST"])
def book_match(request, pk):

    renderer_classes = [userrenderer]
    permission_classes = [IsAuthenticated]
    try:
        # get the instance
        match = Match.objects.get(pk=pk)
        user = request.user
    except Match.DoesNotExist:
        return Response({"error": "Match not found"}, status=status.HTTP_404_NOT_FOUND)
    if match.no_tickets == 0:
        match.avilable = False

    if match.avilable == True:

        serializer = serializers.bookmatchserializer(data=request.data)
        # price =0.0

        if serializer.is_valid():
            price = match.ticket_price * serializer.validated_data.get(
                "tickets_reserved"
            )

            serializer.save(user_id=request.user, match_id=match, price=price)
            x = match.no_tickets
            y = serializer.data.get("tickets_reserved")
            temp_x = x - y
            if temp_x < 0:
                return Response(
                    {
                        "error": [
                            "Not enough tickets",
                            f"you can book up to  {x} tickets only!",
                        ]
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if temp_x == 0:
                match.avilable = False

            if serializer.data.get("pay_method") == "offline":
                # print("yara")
                match.no_tickets = temp_x
                match.save()

                body = render_to_string(
                    "ticket_email\offline_email.html",
                    {
                        "match": match,
                        "numberOfTickets": serializer.data.get("tickets_reserved"),
                        "customerName": user.username,
                        "totalPrice": price,
                    },
                )

                # Send the email
                data = {
                    "subject": f"Ticketaya Match Ticket Confirmation",
                    "body": body,  # Rendered HTML content
                    "to_email": user.email,
                }
                Util.send_email(data)
                return Response(
                    {
                        "message": "The match has been booked successfully, check your email for payment details and ticket receipt date",
                        "reservation": serializer.data,
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {
                        "message": f"the price is {price}",
                        "username": request.user.username,
                        "match_name": match.name,
                        "reservation": serializer.data,
                    },
                    status=status.HTTP_201_CREATED,
                )  # it shouldn't appear in reservation page but must appear in payment page

        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
    else:
        return Response(
            {"error": "Match is not available"}, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["DELETE"])
def cancel_reservation(request, pk):
    renderer_classes = [userrenderer]
    permission_classes = [IsAuthenticated]
    try:
        reservation = match_reservation.objects.get(pk=pk)
    except match_reservation.DoesNotExist:
        return Response(
            {"error": "Reservation not found"}, status=status.HTTP_404_NOT_FOUND
        )
    if reservation.user_id == request.user:
        reservation.delete()
        return Response({"msg": "Reservation cancelled"}, status=status.HTTP_200_OK)
    else:
        return Response(
            {"error": "You are not the owner of this reservation"},
            status=status.HTTP_400_BAD_REQUEST,
        )


# ----------------------------------------------------------------------------------------------------------------
@api_view(["GET"])
def list_all_reservations_for_admin(request):
    renderer_classes = [userrenderer]
    permission_classes = [IsAuthenticated]

    if request.user.is_staff:
        reservations = match_reservation.objects.all()
        serializer = serializers.listadminserializer(reservations, many=True)
        # serializer.data.get()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(
            {"error": "You are not authorized to view this page"},
            status=status.HTTP_401_UNAUTHORIZED,
        )


@api_view(["GET"])
def list_all_reservations_for_user(request):
    renderer_classes = [userrenderer]
    permission_classes = [IsAuthenticated]
    reservations = match_reservation.objects.filter(user_id=request.user)
    serializer = serializers.listuserserializer(reservations, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# ----------------------------------------------------------------------------------------------------------------
@api_view(["PATCH"])
def update_reservation(request, pk):
    renderer_classes = [userrenderer]
    permission_classes = [IsAuthenticated]
    try:
        reservation = match_reservation.objects.get(pk=pk)
    except match_reservation.DoesNotExist:
        return Response(
            {"error": "Reservation not found"}, status=status.HTTP_404_NOT_FOUND
        )
    if reservation.user_id == request.user:
        serializer = serializers.updatereservationserializer(
            reservation, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"msg": ["updated successfully", serializer.data]},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


@api_view(["POST"])
def match_payment(request, pk):
    renderer_classes = [userrenderer]
    permission_classes = [IsAuthenticated]
    try:
        user = request.user
        reservation_id = match_reservation.objects.get(pk=pk)
        match = reservation_id.match_id
    except match_reservation.DoesNotExist:
        return Response(
            {"error": "You already paid for this match"},
            status=status.HTTP_404_NOT_FOUND,
        )
    x = match.no_tickets

    serializer = serializers.matchpaymentserializer(data=request.data)
    if serializer.is_valid():
        serializer.save(
            reservation_id=reservation_id
        )  # Saving the reservation in the payment
        match.no_tickets -= reservation_id.tickets_reserved
        if match.no_tickets < 0:
            return Response(
                {
                    "error": [
                        "Not enough tickets",
                        f"you can book up to  {x} tickets only!",
                    ]
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        if match.no_tickets == 0:
            match.avilable = False
        match.save()
        body = render_to_string(
            "ticket_email\match_ticket_email.html",
            {
                "match": match,
                "numberOfTickets": reservation_id.tickets_reserved,
                "customerName": user.username,
                "totalPrice": reservation_id.price,
            },
        )
        reservation_id.delete()

        # Send the email
        data = {
            "subject": f"Ticketaya Match Ticket Confirmation",
            "body": body,  # Rendered HTML content
            "to_email": user.email,
        }
        Util.send_email(data)
        return Response(
            {"msg": ["Payment done!", serializer.data]}, status=status.HTTP_200_OK
        )
    return Response(serializer.errors, status=status.HTTP_402_PAYMENT_REQUIRED)
