from django.template.loader import render_to_string
from account.utils import Util
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Party
from .serializer import PartySerializer, User_partySerializer, show
from .permissions import IsAdminPermission
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from account.renderers import userrenderer
from rest_framework.permissions import IsAuthenticated
from decimal import Decimal


# -------------------------------(List_Parties)------------------------------------------------------


class PartyListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        parties = Party.objects.all()
        serializer = PartySerializer(parties, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)


# -------------------------------(Delete_Party)------------------------------------------------------


class PartyDeleteView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminPermission]

    def delete(self, request, pk, *args, **kwargs):
        party = get_object_or_404(Party, pk=pk)
        party.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# -------------------------------(Create_Party)------------------------------------------------------


class PartyCreateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminPermission]

    def post(self, request, *args, **kwargs):
        request.data["avilable"] = True
        serializer = PartySerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# -------------------------------(Retrieve_Party)------------------------------------------------------


class PartyRetrieveView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminPermission]

    def get(self, request, pk, *args, **kwargs):
        party = get_object_or_404(Party, pk=pk)
        serializer = PartySerializer(party, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)


# -------------------------------(Update_Party)------------------------------------------------------


class PartyUpdateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminPermission]

    def patch(self, request, pk, *args, **kwargs):
        party = get_object_or_404(Party, pk=pk)
        serializer = PartySerializer(
            party, data=request.data, partial=True, context={"request": request}
        )  # Partial update
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# -------------------------------(Search_Party)------------------------------------------------------


class PartySearchView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminPermission]

    def get(self, request, *args, **kwargs):
        search_query = request.query_params.get("name", "")
        parties = Party.objects.filter(name__icontains=search_query)
        serializer = PartySerializer(parties, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)


# -------------------------------------------------------------------------------------


# -------------------------------(BuyParty Ticket)------------------------------------------------------
class Buyticket(APIView):
    renderer_class = [userrenderer]
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        party = Party.objects.filter(name=request.data["name"]).first()
        if party.number_of_tickets == 0:
            return Response({"message": "SoldOut"})
        if party.number_of_tickets < int(request.data["number_of_tickets"]):
            return Response({"message": "Not available quantity"})
        total = Decimal(request.data["number_of_tickets"]) * party.price
        party.number_of_tickets -= int(request.data["number_of_tickets"])
        data = {"party": party.id, "user": request.user.id, "total": total}
        data2 = {
            "number_of_tickets": party.number_of_tickets,
        }
        data3 = {"name": party.name, "username": request.user.username, "total": total}
        serializerrrr = show(data=data3)

        serializer = User_partySerializer(data=data)

        if serializer.is_valid():
            serializer.save()
        else:
            return Response({"message": "couldn't buy", "errors": serializer.errors})

        serializerr = PartySerializer()
        serializerr.update(party, data2)
        if serializerrrr.is_valid():

            return Response(serializerrrr.data)
        else:
            return Response({"message": "couldn't buy", "errors": serializerrrr.errors})


# ---------------------------------------(party reservation)----------------------------------------------

from .models import Party_reservation
from .serializer import bookpartyserializer, partypaymentserializer
from rest_framework.decorators import api_view


@api_view(["POST"])
def book_party(request, pk):

    renderer_classes = [userrenderer]
    permission_classes = [IsAuthenticated]
    try:
        # get the instance
        party = Party.objects.get(pk=pk)
        user = request.user
    except Party.DoesNotExist:
        return Response({"error": "Party not found"}, status=status.HTTP_404_NOT_FOUND)
    if party.number_of_tickets == 0:
        party.avilable = False

    if party.avilable == True:

        serializer = bookpartyserializer(data=request.data)
        # price =0.0

        if serializer.is_valid():
            price = party.price * serializer.validated_data.get("tickets_reserved")

            serializer.save(user_id=request.user, party_id=party, price=price)
            x = party.number_of_tickets
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
                party.avilable = False

            if serializer.data.get("pay_method") == "offline":
                # print("yara")
                party.number_of_tickets = temp_x
                party.save()

                body = render_to_string(
                  "ticket_email\party_offline.html", 
                  {
                    "party": party,
                    "numberOfTickets": serializer.data.get("tickets_reserved"),
                    "customerName": user.username,
                    "totalPrice": price
                  }
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
                        "message": "The party has been booked successfully, check your email for payment details and ticket receipt date",
                        "reservation": serializer.data,
                    },
                    status=status.HTTP_200_OK,
                )
            else:

                return Response(
                    {
                        "message": f"the price is {price}",
                        "username": request.user.username,
                        "party_name": party.name,
                        "reservation": serializer.data,
                    },
                    status=status.HTTP_201_CREATED,
                )  # it shouldn't appear in reservation page but must appear in payment page

        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
    else:
        return Response(
            {"error": "Party is not available"}, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["POST"])
def Party_payment(request, pk):
    renderer_classes = [userrenderer]
    permission_classes = [IsAuthenticated]
    try:
        user = request.user
        reservation_id = Party_reservation.objects.get(pk=pk)
        party = reservation_id.party_id
    except Party_reservation.DoesNotExist:
        return Response(
            {"error": "You already paid for this party"},
            status=status.HTTP_404_NOT_FOUND,
        )
    x = party.number_of_tickets

    serializer = partypaymentserializer(data=request.data)
    if serializer.is_valid():
        serializer.save(
            reservation_id=reservation_id
        )  # Saving the reservation in the payment
        party.number_of_tickets -= reservation_id.tickets_reserved
        if party.number_of_tickets < 0:
            return Response(
                {
                    "error": [
                        "Not enough tickets",
                        f"you can book up to  {x} tickets only!",
                    ]
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        if party.number_of_tickets == 0:
            party.avilable = False
        party.save()
        body = render_to_string(
          "ticket_email\match_ticket_email.html", 
          {
            "match": party,
            "numberOfTickets": reservation_id.tickets_reserved,
            "customerName": user.username,
            "totalPrice": reservation_id.price
          }
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
