from django.core.validators import MinLengthValidator
from django.db import models
from core.models import User


class TgUser(models.Model):
    tg_chat_id = models.BigIntegerField()
    tg_user_id = models.BigIntegerField(unique=True)
    tg_username = models.CharField(max_length=32, validators=[MinLengthValidator(5)], null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,)
    verification_code = models.CharField(max_length=32, unique=True, null=True, blank=True)
