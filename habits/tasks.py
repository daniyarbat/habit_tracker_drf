import datetime
import requests
from celery import shared_task
from django.conf import settings
from django.utils import timezone
from habits.models import Habit


@shared_task
def habit_operate():
    # print("Task habit_operate started.")
    habits = Habit.objects.all()
    for habit in habits:
        # print(f"Processing habit: {habit}")
        now = datetime.datetime.now()
        now = timezone.make_aware(now, timezone.get_current_timezone())
        if not habit.is_nice and now.hour == habit.time.hour and now.minute == habit.time.minute:
            text = f"Я буду {habit.action} в {habit.time.strftime('%H:%M')} в {habit.place}"
            # print(f"Sending message: {text}")
            user_chat_id = habit.user.chat_id  # Получаем chat_id пользователя из модели User
            send_message(text, user_chat_id)  # Отправляем сообщение с использованием числового chat_id

            if habit.associated_hab:
                text = f"Затем я сделаю: {habit.associated_hab}"
                # print(f"Sending associated habit message: {text}")
                send_message(text, user_chat_id)
            elif habit.reward:
                text = f"Я получу: {habit.reward}"
                # print(f"Sending reward message: {text}")
                send_message(text, user_chat_id)
    # print("Task habit_operate completed.")


def send_message(text, user_chat_id):
    # print(f"Sending message to chat_id {user_chat_id}: {text}")
    url = 'https://api.telegram.org/bot'
    token = settings.TELEBOT_KEY
    requests.post(
        url=f"{url}{token}/sendMessage",
        data={
            "chat_id": user_chat_id,
            "text": text
        }
    )
