from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Party
from .serializer import PartySerializer
from .permissions import IsAdminPermission
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

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
        serializer = PartySerializer(party, data=request.data, partial=True)  # Partial update
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# -------------------------------(Search_Party)------------------------------------------------------

class PartySearchView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminPermission]

    def get(self, request, *args, **kwargs):
        search_query = request.query_params.get('name', '')
        parties = Party.objects.filter(name__icontains=search_query)
        serializer = PartySerializer(parties, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
