from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Meta:
        verbose_name: str = "Пользователь"
        verbose_name_plural: str = "Пользователи"
