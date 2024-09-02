from django.shortcuts import render
from rest_framework import  status
from rest_framework.decorators import api_view
from .  import serializers
from rest_framework.response import Response
from django.http import Http404
from django.contrib.auth import authenticate
from . renderers import userrenderer
from rest_framework_simplejwt.tokens import RefreshToken
from . permissions import  IsAuthOrReadOnly
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.exceptions import ValidationError
from .serializers import UserSerializer
# Create your views here.
# ----------------------(jwt_tokens)-------------------------------------------------
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

# ----------------------(register_view)-------------------------------------------------

@api_view(['POST'])
def register (request):

    if request.method == 'POST':
        renderer_class =  [userrenderer]
        serializer = serializers.userRegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response({'token':token ,'msg':"register successfull"}, status=status.HTTP_201_CREATED)
        return Response (serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# ----------------------(login_view)-------------------------------------------------

@api_view(['POST'])
def  login (request):
    

    if request.method == 'POST':
        renderer_class =  [userrenderer]
        serializer = serializers.userLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            username = serializer.data.get('username')
            password = serializer.data.get('password')
            user = authenticate(username=username, password=password) 

            if user is not None:
                token = get_tokens_for_user(user)
                return Response({'token':token ,'msg':"login successfull"}, status=status.HTTP_200_OK)
            else:
                return Response({'msg':"invalid username or password"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

# ----------------------(userprofile_view)-------------------------------------------------
        
@api_view(['GET'])
def userprofile(request):
    if request.method == 'GET':
        renderer_class =  [userrenderer]
        permission_classes = [IsAuthOrReadOnly]
        serializer = serializers.userProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


# @api_view(['POST'])
# def  change_password(request):
#     if request.method == 'POST':
#         renderer_class =  [userrenderer]
#         serializer = serializers.changepasswordserializers(data=request.data, context={'request': request})

#         if serializer.is_valid(raise_exception=True):
#             old_password = serializer.data.get('old_password')
#             user = authenticate(password=old_password) 
#             if user is not None:
#                 new_password = serializer.data.get('new_password')
#                 user.set_password(new_password)
#                 user.save()
#                 return Response({'msg':"password changed successfull"}, status=status.HTTP_200_OK)
#             else:
#                 return Response ({'msg':"old_password invalid"}, status=status.HTTP_401_UNAUTHORIZED)
        
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     else:
#         return Response({'msg':"invalid request"}, status=status.HTTP_400_BAD_REQUEST)


            
# ----------------------(change_password_view)-------------------------------------------------

@api_view(['POST'])
def change_password(request):
    serializer = serializers.ChangePasswordSerializer(data=request.data, context={'request': request})

    if serializer.is_valid():
        serializer.save()
        return Response({'msg': "Password changed successfully"}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ----------------------(reset_password_email_view)-------------------------------------------------

@api_view(['POST'])
def  reset_password_email(request):
    renderer_classes = [userrenderer]
    serializer = serializers.reset_password_email_serializer(data=request.data)
    if serializer.is_valid(raise_exception = True):
        return Response({'msg':'password resert link was send .please check your email'},status = status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#----------------------------------------------------------------------------------


#add admin

class addadmin(APIView):
    def post(self,request):
        token=request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('not authenticated')
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        raise ValidationError(serializer.errors)

# -------------------------------------------------------------------------------------

# @api_view(['post'])
# def forgotpassword(request):
#     if request.method == 'POST':
#         renderer_class =  [userrenderer]
#         serializer = forgotpasswordSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#             return Response({'msg':"password reset link sent to your email"}, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

        




