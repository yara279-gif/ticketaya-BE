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
from .models import Match

# Create your views here.
# my views is (add match / update match /delete match /retive all/retrive spacific one / search about spacific one )
# ++++++++++++++++++++++++++++++++++++(add_match)+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


@api_view(["POST"])
def addmatch(request):
    if request.method == "POST":
        renderer_class = [userrenderer]
        permission_classes = [IsAuthenticated]
        serializer = serializers.match(data=request.data, context={"request": request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                {"msg": "added successfull", "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ++++++++++++++++++++++++++++++++++++(retrive_all_match)+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


@api_view(["GET"])
def retrieve_all_match(request):
    if request.method == "GET":
        renderer_class = [userrenderer]
        permission_classes = [IsAuthenticated]
        match = Match.objects.all()

        serializer = serializers.match(match, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({"msg": "not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


# ++++++++++++++++++++++++++++++++++++(retrive_one_match)+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
@api_view(["GET"])
def retrieve_one_match(request, pk):
    if request.method == "GET":
        renderer_class = [userrenderer]
        permission_classes = [IsAuthenticated]
        try:
            match = Match.objects.get(pk=pk)
            serializer = serializers.match(match, context={"request": request})
            if match.no_tickets == 0:
                match.avilable = False

                return Response(
                    {
                        "msg": ["This match is not available because all tickets have been sold out",serializer.data]
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Match.DoesNotExist:
            return Response({"msg": "Not found"}, status=status.HTTP_404_NOT_FOUND)

    return Response({"msg": "not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


# ++++++++++++++++++++++++++++++++++++(update_match)+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


@api_view(["PATCH"])
def update_match(request, pk):
    if request.method == "PATCH":
        renderer_class = [userrenderer]
        permission_classes = [IsAuthenticated]
        try:
            match = Match.objects.get(pk=pk)
            serializer = serializers.match(
                match, data=request.data, partial=True, context={"request": request}
            )
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(
                    {"msg": "updated successfully", "data": serializer.data},
                    status=status.HTTP_200_OK,
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Match.DoesNotExist:
            return Response({"msg": "Not found"}, status=status.HTTP_404_NOT_FOUND)
    return Response({"msg": "not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


# ++++++++++++++++++++++++++++++++++++(delete_match)+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


@api_view(["DELETE"])
def deletematch(request, pk):
    if request.method == "DELETE":
        try:
            match = Match.objects.get(pk=pk)
            match.delete()
            return Response(
                {"msg": "deleted successfully"}, status=status.HTTP_204_NO_CONTENT
            )
        except Match.DoesNotExist:
            return Response(
                {"error": "Matcher not found"}, status=status.HTTP_400_BAD_REQUEST
            )


# ++++++++++++++++++++++++++++++++++++(search_about_match)+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
@api_view(["POST"])
def search_about_match(request, name=None, team1=None, team2=None):
    if request.method == "POST":
        renderer_class = [userrenderer]
        permission_classes = [IsAuthenticated]
        name = request.data.get("name")
        team1 = request.data.get("team1")
        team2 = request.data.get("team2")

        if name is None and team1 is None and team2 is None:
            return Response(
                {"msg": "Name of match or name of any team are required for search"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            if name:
                match = Match.objects.filter(name__icontains=name)
            elif team1:
                match = Match.objects.filter(team1__icontains=team1)
            else:
                match = Match.objects.filter(team2__icontains=team2)

            serializer = serializers.match(
                match, many=True, context={"request": request}
            )
            if serializer.data:
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"msg": "No matches found"}, status=status.HTTP_404_NOT_FOUND
                )
        except Match.DoesNotExist as e:
            return Response(
                {"error": f"Match not found {e}"}, status=status.HTTP_404_NOT_FOUND
            )
    return Response({"msg": "not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
