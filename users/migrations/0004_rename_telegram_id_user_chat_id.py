# Generated by Django 5.0.3 on 2024-03-30 10:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_user_telegram_user_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='telegram_id',
            new_name='chat_id',
        ),
    ]
