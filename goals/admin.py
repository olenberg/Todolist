from django.contrib import admin
from goals.models import GoalCategory, Goal, GoalComment


@admin.register(GoalCategory)
class GoalCategoryAdmin(admin.ModelAdmin):
    list_display = ["title", "user", "created", "updated"]
    search_fields = ["title", "user"]
    readonly_fields = ["created", "updated"]
    search_fields = ["title", "user__username"]


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ["user", "category", "title", "status", "priority", "due_date"]
    list_filter = ["status", "priority", "due_date"]
    readonly_fields = ["created", "updated"]
    search_fields = ["title", "user__username"]


@admin.register(GoalComment)
class GoalCommentAdmin(admin.ModelAdmin):
    list_display = ["goal", "user", "created", "updated"]
    search_fields = ["goal__title", "text"]
    readonly_fields = ["created", "updated"]
