from http import server
from urllib import request
from django.shortcuts import render
from rest_framework import status, generics
from rest_framework.decorators import api_view

from account.utils import Util
from . import serializers
from rest_framework.response import Response
from django.http import Http404
from django.contrib.auth import authenticate, logout
from .renderers import userrenderer
from rest_framework_simplejwt.tokens import RefreshToken
from .permissions import IsAuthOrReadOnly
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.exceptions import ValidationError
from .serializers import (
    ListSerializer,
    UserSerializer,
    AdminSerializer,
    userProfileSerializer,
)
from .models import User
from django.template.loader import render_to_string

# ----------------
from django.core.mail import message, send_mail, EmailMessage
from ticketaya.settings import EMAIL_HOST_USER

# Create your views here.
# ----------------------(jwt_tokens)-------------------------------------------------
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


# ----------------------(register_view)-------------------------------------------------


@api_view(["POST"])
def register(request):

    if request.method == "POST":
        renderer_class = [userrenderer]
        serializer = serializers.userRegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            # Render email template
            body = render_to_string("account/wellcome_mail.html", {"user": user})

            # Send the email
            data = {
                "subject": f"Wellcome {user.username} to Ticketaya",
                "body": body,  # Rendered HTML content
                "to_email": user.email,
            }
            Util.send_email(data)
            token = get_tokens_for_user(user)
            return Response(
                {"token": token, "msg": "register successfull"},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ----------------------(login_view)-------------------------------------------------


@api_view(["POST"])
def login(request):

    if request.method == "POST":
        renderer_class = [userrenderer]
        serializer = serializers.userLoginSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid(raise_exception=True):
            username = serializer.data.get("username")
            password = serializer.data.get("password")
            # usr = serializer.data.get('user')
            user = authenticate(username=username, password=password)

            if user is not None:
                is_admin = user.is_admin
                token = get_tokens_for_user(user)
                return Response(
                    {"is_admin": is_admin, "token": token, "msg": "login successfull"},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"msg": "invalid username or password"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ----------------------(userprofile_view)-------------------------------------------------


@api_view(["GET"])
def userprofile(request):
    if request.method == "GET":
        renderer_class = [userrenderer]
        permission_classes = [IsAuthOrReadOnly]
        serializer = serializers.userProfileSerializer(
            request.user, context={"request": request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


# ----------------------(change_password_view)-------------------------------------------------


@api_view(["POST"])
def change_password(request):
    serializer = serializers.ChangePasswordSerializer(
        data=request.data, context={"request": request}
    )
    if serializer.is_valid():

        serializer.save()
        return Response(
            {"msg": "Password changed successfully"}, status=status.HTTP_200_OK
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ----------------------------------------------------------------------------------


# ----------------------(addadmin)-------------------------------------------------


class addadmin(APIView):
    renderer_class = [userrenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializerr = userProfileSerializer(request.user)
        if serializerr.data["is_admin"] == False:
            return Response({"message": "Don't have access"})

        serializer = AdminSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Render email template
            body = render_to_string("account/admin_mail.html", {"user": user})

            # Send the email
            data = {
                "subject": f"New Admin: Wellcome {user.username} to Ticketaya",
                "body": body,  # Rendered HTML content
                "to_email": user.email,
            }
            Util.send_email(data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        raise ValidationError(serializer.errors)


# -------------------------------------------------------------------------------------

# ----------------------(adduser)-------------------------------------------------
class adduser(APIView):
    renderer_class = [userrenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializerr = userProfileSerializer(request.user)
        if serializerr.data["is_admin"] == False:
            return Response({"message": "Don't have access"})
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        raise ValidationError(serializer.errors)


# ----------------------------------------------------------------------------------

# ----------------------(retrieveuser)-------------------------------------------------
class retrieveeuser(APIView):
    renderer_class = [userrenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        serializerr = userProfileSerializer(request.user)
        if serializerr.data["is_admin"] == False:
            return Response({"message": "Don't have access"})

        user = User.objects.filter(id=id).first()
        if not user is None:
            serializer = UserSerializer(user, context={"request": request})
            return Response(serializer.data)
        return Response({"message": "user not found"})


# ----------------------------------------------------------------------------------
# ----------------------(searchuserbyname)-------------------------------------------------
class searchuser(APIView):
    renderer_class = [userrenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request, username):
        serializerr = userProfileSerializer(request.user)
        if serializerr.data["is_admin"] == False:
            return Response({"message": "Don't have access"})

        user = User.objects.filter(username__contains=username)
        if user.exists():
            serializer = UserSerializer(user, many=True, context={"request": request})
            return Response(serializer.data)
        return Response({"message": "user not found"})


# ----------------------------------------------------------------------------------
# ----------------------(deleteuser)-------------------------------------------------
class deleteuser(APIView):
    renderer_class = [userrenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        serializerr = userProfileSerializer(request.user)
        if serializerr.data["is_admin"] == False:
            return Response({"message": "Don't have access"})
        user = User.objects.filter(id=id).first()
        if user:
            user.delete()
            return Response({"message": "deleted succesfully"})
        return Response({"message": "user not found"})


# ----------------------------------------------------------------------------------
# ----------------------(updateuser)-------------------------------------------------
class updateuser(APIView):
    renderer_class = [userrenderer]
    permission_classes = [IsAuthenticated]

    def patch(self, request, id):
        serializerr = userProfileSerializer(request.user)
        if serializerr.data["is_admin"] == False:
            return Response({"message": "Don't have access"})
        user = User.objects.filter(id=id).first()
        if user:
            serializer = UserSerializer()
            serializer.update(user, request.data)
            return Response({"message": "updated succesfully"})
        return Response({"message": "user not found"})


# ----------------------------------------------------------------------------------
# ----------------------(listuser)-------------------------------------------------
class listusers(APIView):
    renderer_class = [userrenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializerr = userProfileSerializer(request.user)
        if serializerr.data["is_admin"] == False:
            return Response({"message": "Don't have access"})

        user = User.objects.all()
        if not user:
            return Response({"message": "There is no users"})

        serializer = ListSerializer(user, many=True, context={"request": request})
        return Response(serializer.data)


# -------------------------------(logout)------------------------------------------------------
@api_view(["GET", "POST"])
def user_logout(request):
    renderer_class = [userrenderer]
    permission_classes = [IsAuthenticated]
    try:
        refresh_token = request.data["refresh_token"]
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({"msg": "Logged out successfully"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"msg": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)


# --------------------------------------(user_delete_account)-----------------------------------------------------------


@api_view(["DELETE"])
def delete_account(request):
    renderer_class = [userrenderer]
    permission_classes = [IsAuthenticated]
    try:
        user = request.user
        user.delete()
        return Response(
            {"msg": "Account deleted successfully"}, status=status.HTTP_200_OK
        )
    except Exception as e:
        return Response(
            {"msg": "Failed to delete account"}, status=status.HTTP_400_BAD_REQUEST
        )


# ------------------------------------------------------------------------------------------
# -------------------------------(user_update_profile)-------------------------------------------
@api_view(["GET", "PUT"])
def update_profile(request):
    renderer_class = [userrenderer]
    permission_classes = [IsAuthenticated]
    if request.method == "GET":
        serializer = serializers.updateuserprofileserializer(
            request.user, context={"request": request}
        )

        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "PUT":
        count = 0
        existing_data = serializers.updateuserprofileserializer(
            request.user, context={"request": request}
        ).data
        y = existing_data.values()
        y = list(y)
        print(type(y))
        print(y)

        serializer = serializers.updateuserprofileserializer(
            request.user, data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            x = serializer.data.values()
            keys = serializer.data.keys()
            keys = list(keys)
            x = list(x)
            print(type(x))
            print(x)
            ls = []
            for i in range(5):
                if y[i] == x[i]:
                    continue
                else:
                    ls.append(f"{keys[i]} updated successfully")
                    count += 1
            if count == 0:
                return Response(
                    {"msg": "No changes made"}, status=status.HTTP_406_NOT_ACCEPTABLE
                )
            return Response({"msg": ls}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# -----------------------------------------------------------------------------------------


# -------------------------------(sendResetPasswordPage)-------------------------------------------

from .models import Profile
from django.http import HttpResponse


@api_view(["GET"])
def sendResetPasswordPage(request, uid, token):
    renderer_class = [userrenderer]

    try:
        profile = Profile.objects.get(reset_password_token=token)
        user = profile.user
    except Profile.DoesNotExist:
        user = None

    if user is not None and profile.reset_password_token == token:

        return render(
            request, "account/reset_password.html", {"token": token, "uid": uid}
        )
    else:
        return HttpResponse("Password reset link is invalid or has expired.")


# ----------------------------------------------------------------------------------
# -------------------------------(resert_password)----------------------------------
@api_view(["POST"])
def reset_password(request, uid, token):
    renderer_class = [userrenderer]
    serializer = serializers.ResetPasswordSerializer(
        data=request.data, context={"uid": uid, "token": token}
    )
    try:
        if serializer.is_valid(raise_exception=True):
            return render(
                request,
                "account/reset_password.html",
                {
                    "success_message": "Password has been reset successfully. go to login page"
                },
            )
    except Exception as e:
        return render(
            request,
            "account/reset_password.html",
            {
                "error_message": "Expired link of Rest Password \n please go to forget password page."
            },
        )


# ----------------------------------------------------------------------------------
# ----------------------(reset_password_email_view)-------------------------------------------------


@api_view(["POST"])
def reset_password_email(request):
    renderer_classes = [userrenderer]
    serializer = serializers.ResetPasswordEmailSerializer(
        data=request.data, context={"request": request}
    )
    if serializer.is_valid(raise_exception=True):
        return Response(
            {"msg": "password resert link was send .please check your email"},
            status=status.HTTP_200_OK,
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
