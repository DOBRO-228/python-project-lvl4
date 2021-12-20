from django.db import models
from statuses.models import Status
from django.contrib.auth.models import User


class Task(models.Model):
    name = models.CharField(max_length=150, blank=False)
    description = models.TextField()
    author = models.ForeignKey(User, related_name='author', blank=True, null=True, on_delete=models.SET_NULL)
    status = models.ForeignKey(Status, blank=True, null=True, on_delete=models.SET_NULL)
    performer = models.ForeignKey(User, related_name='performer', blank=True, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

    def __str__(self):
        return self.name
