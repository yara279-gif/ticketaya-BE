from turtle import isvisible
from django.shortcuts import render
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
        serializer = PartySerializer(parties, many=True)
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
        serializer = PartySerializer(data=request.data)
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
        serializer = PartySerializer(party)
        return Response(serializer.data, status=status.HTTP_200_OK)


# -------------------------------(Update_Party)------------------------------------------------------


class PartyUpdateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminPermission]

    def patch(self, request, pk, *args, **kwargs):
        party = get_object_or_404(Party, pk=pk)
        serializer = PartySerializer(
            party, data=request.data, partial=True
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
        serializer = PartySerializer(parties, many=True)
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
