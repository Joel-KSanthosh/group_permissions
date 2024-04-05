from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import PermissionsMixin,BaseUserManager,AbstractBaseUser
from django.utils import timezone
# Create your models here.

class UserManager(BaseUserManager):

    def _create_user(self,username,email,password,role,is_staff,is_superuser,**extra_fields):
        if not email:
            raise ValueError("User must have an Email address")
        now=timezone.now()
        email = self.normalize_email(email).lower()
        user=self.model(
            username=username.lower(),
            email=email,
            role=role,
            is_staff=is_staff,
            is_superuser=is_superuser,
            last_login=now,
            date_joined=now,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self,username,email,role,password,**extra_fields):
        return self._create_user(username,email,role,password,False,False,**extra_fields)
    
    def create_staffuser(self,username,email,role,password,**extra_fields):
        user=self._create_user(username,email,role,password,True,False,**extra_fields)
        return user
    
    def create_superuser(self,username,email,role,password,**extra_fields):
        user=self._create_user(username,email,role,password,True,True,**extra_fields)
        return user

class User(AbstractUser):
    email = models.EmailField(unique=True, max_length=50)
    username = models.CharField(unique=True, max_length=20)

    # ROLES
    OWNER = 1
    CUSTOMER = 2
    EMPLOYEE = 3
    ROLE_CHOICES = (
        (OWNER, "Owner"),
        (CUSTOMER, 'Customer'),
        (EMPLOYEE, 'Employee'),
    )
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True)


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email
    

