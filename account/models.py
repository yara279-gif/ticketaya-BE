from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email,username,first_name,last_name ,  password=None,password2= None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        
        if not email:
            raise ValueError("Users must have an email address")
       
        user = self.model(
            email=self.normalize_email(email),
            username = username,
            first_name =first_name,
            last_name =last_name

        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email, username, first_name,last_name , password=None):
        """
        Creates and saves a superuser with the given email,username,  first/last name
         and password.
        """
        user = self.create_user(
            email,
            username= username, 
            password=password,
            first_name= first_name,
            last_name = last_name,
            # is_admin =  False



        )
        #user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="Email",
        max_length=255,
        unique=True,
    )
    username = models.CharField(max_length=255, unique=True)
    first_name =  models.CharField(max_length=255)
    last_name =  models.CharField(max_length=255)
    
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False,null=True,blank= True)

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email","first_name","last_name"]

    def str(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_authenticated

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app app_label?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin