import string
import random
from django.db import models
from core.models import User


class TgUser(models.Model):
    tg_id = models.BigIntegerField(verbose_name="tg id", unique=True)
    tg_chat_id = models.BigIntegerField(verbose_name="tg chat id")
    username = models.CharField(max_length=32, verbose_name="tg username", null=True, blank=True, default=None)
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.PROTECT, null=True, blank=True,
                             default=None)
    verification_code = models.CharField(max_length=12, verbose_name="Код подтверждения")

    class Meta:
        verbose_name = "Telegram пользователь"
        verbose_name_plural = "Telegram пользователи"

    def set_verification_code(self):
        self.verification_code = "".join(random.choice(string.ascii_letters + string.digits) for _ in range(12))
