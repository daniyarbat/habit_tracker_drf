from django.db import models
from django.conf import settings

NULLABLE = {'null': True, 'blank': True}


class Habit(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name='пользователь', **NULLABLE)
    place = models.CharField(max_length=200, verbose_name='место')
    time = models.TimeField(verbose_name='время')
    action = models.CharField(max_length=300, verbose_name='действие')
    is_nice = models.BooleanField(default=False, verbose_name='признак приятной привычки')
    associated_hab = models.ForeignKey('self', on_delete=models.SET_NULL, verbose_name='связанная привычка', **NULLABLE)
    period = models.PositiveIntegerField(default=1, verbose_name='периодичность')
    reward = models.CharField(max_length=200, verbose_name='вознаграждение', **NULLABLE)
    action_time = models.PositiveIntegerField(verbose_name='время выполнения привычки', **NULLABLE)
    is_public = models.BooleanField(default=False, verbose_name='признак публичности')
    good_habit = models.BooleanField(default=False, verbose_name='полезная привычка')

    def __str__(self):
        return f'{self.action} - {self.time}'

    class Meta:
        verbose_name = 'привычка'
        verbose_name_plural = 'привычки'
