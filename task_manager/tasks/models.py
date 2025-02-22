from django.db import models
from task_manager.users.models import User
from task_manager.statuses.models import Status


class Task(models.Model):
    name = models.CharField(max_length=255, verbose_name="Имя")
    description = models.TextField(verbose_name="Описание", blank=True)
    status = models.ForeignKey(
        Status, on_delete=models.PROTECT,
        verbose_name="Статус")
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name="tasks_created", verbose_name="Автор")
    executor = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name="tasks_assigned",
        null=True, blank=True, verbose_name="Исполнитель")
    labels = models.ManyToManyField(
        'labels.Label', blank=True, related_name='tasks', verbose_name="Метка")
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Создан")

    class Meta:
        verbose_name = "Tasks"
        verbose_name_plural = "Tasks"

    def __str__(self):
        return self.name
