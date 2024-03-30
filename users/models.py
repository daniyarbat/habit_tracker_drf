from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Email')
    name = models.CharField(max_length=50, verbose_name='Имя', **NULLABLE)
    telegram_id = models.TextField(verbose_name='id чата в телеге', **NULLABLE)
    telegram_user_name = models.CharField(max_length=200, verbose_name='имя в телеге', unique=True, **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
