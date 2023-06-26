from core.models import User
from django.db import models
# from django.utils import timezone


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated = models.DateTimeField(auto_now=True, verbose_name="Дата последнего обновления")

    class Meta:
        abstract = True

    # class Meta:
    #     abstract: bool = True
    #
    # def save(self, *args, **kwargs) -> None:
    #     if not self.pk:
    #         self.created = timezone.now()
    #     self.updated = timezone.now()
    #
    #     return super().save(*args, **kwargs)


class GoalCategory(BaseModel):
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    title = models.CharField(verbose_name="Название", max_length=255)
    user = models.ForeignKey(
        User, verbose_name="Автор", on_delete=models.PROTECT
    )
    is_deleted = models.BooleanField(verbose_name="Удалена", default=False)


class Goal(BaseModel):
    class Meta:
        verbose_name = 'Цель'
        verbose_name_plural = 'Цель'

    class Status(models.IntegerChoices):
        to_do = 1, "К выполнению"
        in_progress = 2, "В процессе"
        done = 3, "Выполнено"
        archived = 4, "Архив"

    class Priority(models.IntegerChoices):
        low = 1, "Низкий"
        medium = 2, "Средний"
        high = 3, "Высокий"
        critical = 4, "Критический"

    user = models.ForeignKey(User, verbose_name="Автор", related_name="goals", on_delete=models.PROTECT)
    category = models.ForeignKey(
        GoalCategory,
        verbose_name="Категория",
        on_delete=models.PROTECT,
        related_name="goals",
    )
    title = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField(verbose_name="Описание", null=True, blank=True)
    status = models.PositiveSmallIntegerField(
        verbose_name="Статус", choices=Status.choices, default=Status.to_do
    )
    priority = models.PositiveSmallIntegerField(
        verbose_name="Приоритет", choices=Priority.choices, default=Priority.medium)
    due_date = models.DateField(verbose_name="Дата дедлайна", null=True, blank=True)


class GoalComment(BaseModel):
    class Meta:
        verbose_name = "Комментарий к цели"
        verbose_name_plural = "Комментарии к целям"

    goal = models.ForeignKey(Goal, verbose_name="Цель", on_delete=models.PROTECT)
    user = models.ForeignKey(User, verbose_name="Автор ", on_delete=models.PROTECT)
    text = models.TextField(verbose_name="Текст")
