from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser, PermissionsMixin)
from django.db import models
from django.utils import timezone

class UserManager (BaseUserManager) :
    
    def create_user (self, username, email, identity, school, profile, introduce, password=None) :

        if username is None :
            raise TypeError('Users should have a username')

        if email is None :
            raise TypeError('Users should have a email')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            identity=identity,
            school=school,
            profile=profile,
            introduce=introduce,
        )
        
        user.set_password(password)
        user.save()
        
        return user

    def create_superuser (self, username, email, identity, school, profile, introduce, password=None) :

        if password is None :
            raise TypeError('Password should not be none')

        user = self.create_user(
            username,
            email,
            identity,
            password,
            school,
            profile,
            introduce,
        )
        
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user

class User (AbstractBaseUser, PermissionsMixin) :
    username = models.CharField(max_length=255, unique=True, db_index=True)
    email = models.CharField(max_length=255, unique=True, db_index=True)
    is_verified = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    identity = models.CharField(max_length=6, choices=(('senior', 'senior'), ('junior', 'junior')))
    school = models.CharField(max_length=255)
    profile = models.ImageField(null=True, blank=True)
    introduce = models.CharField(null=True, max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'identity', 'school', 'profile', 'introduce']

    objects = UserManager()

    def __str__ (self) :
        return self.email