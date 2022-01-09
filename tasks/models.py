from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _
from labels.models import Label
from statuses.models import Status


class Task(models.Model):
    name = models.CharField(max_length=150, blank=False, verbose_name=_('Name'))  # Noqa: WPS432
    description = models.TextField(blank=True, verbose_name=_('Description'))
    author = models.ForeignKey(
        User, related_name='created_tasks', blank=False, null=False, on_delete=models.PROTECT, verbose_name=_('Author'),
    )
    status = models.ForeignKey(
        Status, related_name='tasks', blank=False, null=True, on_delete=models.PROTECT, verbose_name=_('Status'),
    )
    performer = models.ForeignKey(
        User,
        related_name='assigned_tasks',
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        verbose_name=_('Performer'),
    )
    labels = models.ManyToManyField(Label, related_name='tasks', blank=True, verbose_name=_('Labels'))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta(object):
        verbose_name = _('Task')
        verbose_name_plural = _('Tasks')

    def __str__(self):
        return self.name
