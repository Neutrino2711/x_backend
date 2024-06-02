from django.db import models

# Create your models here.
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

# from decimal import Decimal

# from io import BytesIO
# from PIL import Image
import os 

from django.core.files.base import ContentFile
from django.conf import settings


class UserManager(BaseUserManager):
    def create_user(self,email,password=None,**extra_fields):
        print('Creating user in UserManager')
        '''
        Creates and saves a new user
        '''

        if not email:
            raise ValueError("User must have an email address")
        
        email = self.normalize_email(email)
        # username = self.model.normalize_username(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password) #encryptes the password
        user.save(using = self._db) #standard procedure for saving objects in django
        return user
    
    def create_superuser(self,email,password):
        '''
        Creates and saves a new superuser
        '''
        user = self.create_user(email,password)
        user.is_superuser = True #is_superuser is created by PermissionMixin
        user.is_staff = True #is_staff is created by PermissionMixin
        user.save(using = self._db)
        return user
    



class User(AbstractBaseUser,PermissionsMixin):
    '''
    Custom user model that supports using email instead of username
    '''
    from django.contrib.auth.models import Group, Permission


    # ... User.user is auth model (settings.py)
    # groups = models.ManyToManyField(Group, related_name='custom_user_groups')
    # user_permissions = models.ManyToManyField(Permission, related_name='custom_user_permissions')
    # ...
    email = models.EmailField(max_length = 255,unique = True)

    name = models.CharField(max_length = 255,null = True)
    city = models.CharField(max_length = 255,null = True)
    dob = models.DateField(null = True)
    bio = models.CharField(max_length = 500,null=True)
    # current timestamp defaults
    joined = models.DateField(auto_now =True)
    profile_pic = models.ImageField(
        null= True,
        blank = True
    )
    # we can access methods of class UserManager() 
    


    is_active = models.BooleanField(default = True)
    is_staff = models.BooleanField(default = False)

   

    

    followers = models.ManyToManyField('self', related_name='following', symmetrical=False)
     
    objects = UserManager()
    
    USERNAME_FIELD = "email"

  

    def follow(self, user):
        self.following.add(user)

    def unfollow(self, user):
        self.following.remove(user)