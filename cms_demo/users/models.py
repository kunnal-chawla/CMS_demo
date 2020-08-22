from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework.authtoken.models import Token

from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
        This class represents the custom user model which extends from django
        AbstractBaseUser model
        This model is design to uniquely identify a user through email id.
    """
    email = models.EmailField(_('email address'), unique=True)
    full_name = models.CharField(max_length=50)
    mobile_number = models.IntegerField(default=0)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=30)
    pin_code = models.IntegerField(default=0)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    """
    This function is a django signal receiver which gets triggered before a
    CustomUser instance is saved to generate token
    """
    if created:
        Token.objects.create(user=instance)


class Content(models.Model):
    """
        This model is designed to keep all the users which belongs to Author
        groups for content creation
    """
    # TODO rename user as created_by in future for better relation of models
    user = models.ForeignKey(CustomUser, related_name='content_user', on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    body = models.TextField()
    summary = models.TextField()
    document = models.FileField(upload_to='images/')
