from django.contrib.auth.models import User
from django.db import models
from statuses.models import Status


class Task(models.Model):
    name = models.CharField(max_length=150, blank=False)
    description = models.TextField(blank=True)
    author = models.ForeignKey(User, related_name='created_tasks', blank=False, null=True, on_delete=models.SET_NULL)
    status = models.ForeignKey(Status, blank=False, null=True, on_delete=models.SET_NULL)
    performer = models.ForeignKey(User, related_name='assigned_tasks', blank=True, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

    def __str__(self):
        return self.name
