from django.db import models


class Label(models.Model):
    name = models.CharField(max_length=100, unique=True, blank=False, verbose_name='Имя')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Метка'
        verbose_name_plural = 'Метки'

    def __str__(self):
        return self.name
