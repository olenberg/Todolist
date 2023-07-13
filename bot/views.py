from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from bot.models import TgUser
from bot.serializers import BotVerifyCodeUpdateView


class BotVerifyCodeUpdate(generics.UpdateAPIView):
    model = TgUser
    serializer_class = BotVerifyCodeUpdateView
    http_method_names = ['patch']
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(TgUser, verification_code=self.request.data['verification_code'])
