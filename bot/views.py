from django.conf import settings
from rest_framework import permissions
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from bot.models import TgUser
from bot.serializers import TgUserSerializer
from bot.tg.client import TgClient


class VerificationView(GenericAPIView):
    model = TgUser
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TgUserSerializer

    def patch(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        tg_user = serializer.validated_data["tg_user"]
        tg_user.user = self.request.user
        tg_user.save(update_fields=["user"])

        instance_s = self.get_serializer(tg_user)

        tg_client = TgClient(settings.BOT_TOKEN)
        tg_client.send_message(tg_user.tg_chat_id, "Вход прошел успешно!")

        return Response(instance_s.data)