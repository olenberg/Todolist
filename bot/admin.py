from django.contrib import admin
from bot.models import TgUser


# @admin.register(TgUser)
# class TgUserAdmin(admin.ModelAdmin):
#     list_display = ["chat_id", "user"]
#     readonly_fields = ["verification_code"]
#     search_fields = ["chat_id"]
admin.site.register(TgUser)
