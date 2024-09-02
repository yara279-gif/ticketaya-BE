from rest_framework import serializers
from . models import User
from django.contrib.auth import get_user_model
from  django.contrib.auth.password_validation import validate_password
from django.utils.encoding import smart_str,force_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from  django.contrib.auth.tokens import PasswordResetTokenGenerator

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


class reset_password_email_serializer (serializers.ModelSerializer):
    email = serializers.EmailField(max_length = 255)
    class Meta :
        model = User
        fields = ['id','email']
    
    def validate(self, attrs):
        if User.objects.filter(email = attrs['email']).exists():
            user = User.objects.get (email = attrs['email'])
        
            uid = urlsafe_base64_encode(force_bytes(user.id))
            print("'uid",uid)
            token = PasswordResetTokenGenerator().make_token(user)
            print("token",token)
            link = 'http://127.0.0.1:8000/api/user/reset/'+uid+'/'+token
            print("link",link)
            return attrs
        else:
            raise serializers.ValidationError({'email':'user not found'})
        
        


 


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

        




