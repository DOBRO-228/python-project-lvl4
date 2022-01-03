from django.contrib.auth.models import User
from django.db import models
from statuses.models import Status
from labels.models import Label


class Task(models.Model):
    name = models.CharField(max_length=150, blank=False)
    description = models.TextField(blank=True)
    author = models.ForeignKey(User, related_name='created_tasks', blank=False, null=True, on_delete=models.PROTECT)
    status = models.ForeignKey(Status, related_name='tasks', blank=False, null=True, on_delete=models.PROTECT)
    performer = models.ForeignKey(User, related_name='assigned_tasks', blank=True, null=True, on_delete=models.PROTECT)
    label = models.ManyToManyField(Label, related_name='tasks', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

    def __str__(self):
        return self.name
