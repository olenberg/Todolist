from django.urls import path

from bot.views import BotVerifyCodeUpdate

urlpatterns = [
    path('verify', BotVerifyCodeUpdate.as_view(), name='bot_verify_code'),
]
