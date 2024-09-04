from rest_framework import serializers
from . models import User
from django.contrib.auth import get_user_model
from  django.contrib.auth.password_validation import validate_password
from django.utils.encoding import smart_str,force_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from  django.contrib.auth.tokens import PasswordResetTokenGenerator
from .utils import Util
from django.conf import settings

#make instance (object) from the class User
user = User()



# ---------------------------------(register)-------------------------------------

class userRegisterSerializer (serializers.ModelSerializer):

    password2 = serializers.CharField(style ={'input_type':'password'})

    class Meta :
        model = User
        fields = ['email','username','first_name','last_name','password','password2','is_admin']
        extra_kwargs = {
            'password':{'write_only':True}
        }
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password2':'password dont match'})
        return super().validate(attrs)
    
    def create (self, validated_data):
        validated_data.pop('password2')
        return User.objects.create_user(**validated_data)
    

# ---------------------------------(login)-------------------------------------
    
class userLoginSerializer (serializers.ModelSerializer):
    username = serializers.CharField(max_length = 255)
    class Meta :
        model = User
        fields = ['username','password']

# ---------------------------------(user-profile)-------------------------------------

class userProfileSerializer (serializers.ModelSerializer):
    class Meta :
        model = User
        fields = ['id','email','username','first_name','last_name']

# ---------------------------------(change-password)-------------------------------------
class ChangePasswordSerializer(serializers.ModelSerializer):
    #make fields i want to enter it  in the form

    old_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    new_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    confirm_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['old_password', 'new_password', 'confirm_password']

    def validate(self, attrs):
        #get the user from the request
        #user = request.user
        user = self.context['request'].user

        # Check that the old password is correct
        if not user.check_password(attrs['old_password']):
            raise serializers.ValidationError({"old_password": "Old password is incorrect."})

        # Check that new_password and confirm_password match
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "New password doesn't match confirm password."})

        return attrs

    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user
    
# ---------------------------------(reset-password-email)-------------------------------------


class ResetPasswordEmailSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = User
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'email': 'User not found'})

        user = User.objects.get(email=email)
        uid = urlsafe_base64_encode(force_bytes(user.id))
        token = PasswordResetTokenGenerator().make_token(user)
        link = f'http://127.0.0.1:8000/api/user/reset/{uid}/{token}'

        # Log the link for debugging (can be removed in production)
        print(f"Password reset link: {link}")

        # Send the email
        data = {
            'subject': 'Reset your password',
            'body': f"Click the following link to reset your password: {link}",
            'to_email': user.email
        }
        Util.send_email(data)

        return attrs
        

# ---------------------------------(addadmin)-------------------------------------

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','username','first_name','last_name','is_admin','email','password']
        
# password myzhr4
        extra_kwargs={
            'password':{'write_only':True},
            
        }
        #to hash the password
    def create(self, validated_data):
        validated_data['is_admin']=True
        password=validated_data.pop('password',None)
        instance=self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    
#----------------------------(reset_password_serializer)---------------------------------------

class ResetPasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    confirm_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['password', 'confirm_password']

    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')
        uid = self.context.get('uid')
        token = self.context.get('token')

        if password != confirm_password:
            raise serializers.ValidationError({"password": "Passwords do not match"})

        try:
            # Decode the user ID from the UID and retrieve the user
            user_id = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id=user_id)

            # Check if the provided token is valid for the user
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise serializers.ValidationError({'token': 'Token is invalid or has expired'})

            # Set the new password and save the user
            user.set_password(password)
            user.save()

            return attrs

        except (DjangoUnicodeDecodeError, User.DoesNotExist) as e:
            raise serializers.ValidationError({'token': 'Token is invalid or has expired'})
            


#---------------------------------------------------------------------------------------------------
 
        



# class changepasswordserializers (serializers.ModelSerializer):
#     old_password = serializers.CharField(style ={'input_type':'password'}, write_only=True)
#     new_password = serializers.CharField(style ={'input_type':'password'}, write_only=True)
#     confirm_password = serializers.CharField(style ={'input_type':'password'}, write_only=True)
#     class Meta :
#         model = User
#         fields = ['old_password','new_password','confirm_password']
        
#         def validate (self,attrs):

#             user = self.context['user']
#             if attrs['new_password'] != attrs['confirm_password']:
#                 raise serializers.ValidationError({'confirm_password':'new_password doesn\'t match confirm_password'})
#             return 
            
            
            

            

       

# ------------------------------------------------------------------------------------------------------------
# class ChangePasswordSerializer(serializers.Serializer):
#     old_password = serializers.CharField(style={'input_type': 'password'}, max_length=255, write_only=True)
#     password = serializers.CharField(style={'input_type': 'password'}, max_length=255, write_only=True)
#     password2 = serializers.CharField(style={'input_type': 'password'}, max_length=255, write_only=True)

#     def validate(self, attrs):
#         user = self.context['user']

#         # Check if old password is correct
#         if not user.check_password(attrs['old_password']):
#             raise serializers.ValidationError({"old_password": "Old password is incorrect."})

#         # Check if new passwords match
#         if attrs['password'] != attrs['password2']:
#             raise serializers.ValidationError({"password2": "Passwords do not match."})

#         return attrs

#     def save(self):
#         user = self.context['user']
#         user.set_password(self.validated_data['password'])
#         user.save()
#         return user

        




