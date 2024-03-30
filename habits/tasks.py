import datetime

import requests
from celery import shared_task
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

from habits.models import Habit
from users.models import User


@shared_task
def habit_operate():
    check_updates()
    habits = Habit.objects.all()
    for habit in habits:
        now = datetime.datetime.now()
        now = timezone.make_aware(now, timezone.get_current_timezone())
        if not habit.is_nice and now.hour == habit.time.hour and now.minute == habit.time.minute:
            text = f"Я буду {habit.action} в {habit.time.strftime('%H:%M')} в {habit.place}"

            send_message(text, habit.user.chat_id)
            if habit.associated_hab:
                text = f"Затем я сделаю: {habit.associated_hab}"
                send_message(text, habit.user.chat_id)
            elif habit.reward:
                text = f"Я получу: {habit.reward}"
                send_message(text, habit.user.chat_id)


def send_message(text, user_chat_id):
    url = 'https://api.telegram.org/bot'
    token = settings.TELEBOT_KEY
    requests.post(
        url=f"{url}{token}/sendMessage",
        data={
            "chat_id": user_chat_id,
            "text": text
        }
    )


def check_updates():
    get_updates = f"https://api.telegram.org/bot{settings.TELEBOT_KEY}/getUpdates"
    response = requests.get(get_updates)

    if response.status_code == 200:
        for all_telegram_users in response.json()["result"]:
            telegram_user_chat_id = all_telegram_users["message"]["from"]["id"]
            telegram_user_name = all_telegram_users["message"]["from"]["username"]

            try:
                user = User.objects.get(telegram_user_name=telegram_user_name)
                if user.chat_id is None:
                    user.chat_id = telegram_user_chat_id
                    user.save()
            except ObjectDoesNotExist:
                print("Пользователь не найден в базе данных.")
