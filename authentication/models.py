from django.db import models
from django.contrib.auth.models import AbstractBaseUser,  UserManager
from django.core.validators import RegexValidator

# Create your models here.


class User(AbstractBaseUser):
    email = models.EmailField(unique=True, max_length=255, verbose_name="Email address")
    username = models.CharField(max_length=50, unique=False)
    phone_number = models.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                regex=r"^\+?1?\d{9,15}$",
                message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.",
            )
        ],
        unique=True,
        null=False,
        blank=False,
    )

    address = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    password = models.CharField(null=False, blank=False, max_length=128)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "phone_number"]