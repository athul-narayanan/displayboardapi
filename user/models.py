"""
This file contains database models
"""
from django.db import models
from django.contrib.auth.models import(
    AbstractBaseUser,
    BaseUserManager,
)

class UserManager(BaseUserManager):
    """
    Manager class for User model
    """
    def create_user(self, email, password, **extrafields):
        user = self.model(email=email, **extrafields)
        user.set_password(password)
        user.save()

        return user


class UserRole(models.Model):
    """
    This model defines user role in the system
    """

    class Meta:
        db_table = 'userrole'

    role_name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.role_name

class User(AbstractBaseUser):
    """
    This model defines user in the system
    """
    class Meta:
        db_table = 'user' 
        
    firstname = models.CharField(max_length=255)
    initial = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    role = models.ForeignKey(UserRole, on_delete=models.CASCADE, default=1)
    ping_started = models.BooleanField(default=False)
    objects = UserManager()
    

    USERNAME_FIELD = 'email'

class UserSchedules(models.Model):
    """
    This model defines user schedules in the system
    """
    title = models.CharField(max_length=255)
    start = models.DateTimeField()
    end = models.DateTimeField()
    color = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)