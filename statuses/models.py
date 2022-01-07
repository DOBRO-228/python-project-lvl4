from django.db import models


class Status(models.Model):
    name = models.CharField(max_length=100, unique=True, blank=False, verbose_name='Имя')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta(object):
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'

    def __str__(self):
        return self.name
