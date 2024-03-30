from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from habits.models import Habit
from users.models import User


class HabitAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='test@test.pro')
        self.user.set_password('qwe12345')
        self.user.save()
        self.client.force_authenticate(user=self.user)
        self.habit = Habit.objects.create(
            user=self.user,
            place='Место',
            time='21:30:00',
            action='Действие',
            is_nice=False,
            period=1,
            reward='Вознаграждение',
            action_time=110,
            is_public=True,
        )

    def test_habit_create(self):
        data = {
            'user': self.user.id,
            'place': 'Новое место',
            'time': '19:28:00',
            'action': 'Новое действие',
            'is_nice': False,
            'period': 3,
            'reward': '',
            'action_time': 105,
            'is_public': True,
        }
        response = self.client.post(reverse('habits:habit_create'), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 2)

    def test_habit_list(self):
        response = self.client.get(reverse('habits:habit_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(),
                         {
                             'count': 1,
                             'next': None,
                             'previous': None,
                             'results': [
                                 {
                                     'id': self.habit.id,
                                     'user': self.habit.user.id,
                                     'place': self.habit.place,
                                     'time': self.habit.time,
                                     'action': self.habit.action,
                                     'is_nice': self.habit.is_nice,
                                     'associated_hab': self.habit.associated_hab,
                                     'reward': self.habit.reward,
                                     'action_time': self.habit.action_time,
                                     'good_habit': self.habit.good_habit,
                                     'is_public': self.habit.is_public,
                                     'period': self.habit.period,

                                 }
                             ]
                         })

    def test_habit_detail(self):
        response = self.client.get(reverse('habits:habit_detail', args=[self.habit.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(),
                         {
                             'id': self.habit.id,
                             'user': self.habit.user.id,
                             'place': self.habit.place,
                             'time': self.habit.time,
                             'action': self.habit.action,
                             'is_nice': self.habit.is_nice,
                             'associated_hab': self.habit.associated_hab,
                             'reward': self.habit.reward,
                             'action_time': self.habit.action_time,
                             'good_habit': self.habit.good_habit,
                             'is_public': self.habit.is_public,
                             'period': self.habit.period,
                         })

    def test_habit_update(self):
        data = {
            'place': 'Изменение места',
            'time': '10:45:00',
            'action': 'Изменение действия',
            'is_nice': True,
            'period': 7,
            'action_time': 65,
            'is_public': True,
        }
        response = self.client.put(reverse('habits:habit_update', args=[self.habit.id]), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(),
                         {
                             'id': self.habit.id,
                             'user': self.habit.user.id,
                             'place': data['place'],
                             'time': data['time'],
                             'action': data['action'],
                             'is_nice': data['is_nice'],
                             'associated_hab': self.habit.associated_hab,
                             'reward': self.habit.reward,
                             'action_time': data['action_time'],
                             'good_habit': self.habit.good_habit,
                             'is_public': data['is_public'],
                             'period': data['period'],
                         })

    def test_habit_destroy(self):
        response = self.client.delete(reverse('habits:habit_delete', args=[self.habit.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.count(), 0)

    def test_habit_validation(self):
        data = {
            'user': self.user.id,
            'place': 'Еще одно место',
            'time': '03:00:00',
            'action': 'Еще одно действие',
            'is_nice': True,
            'period': 1,
            'reward': 'Еще одно вознаграждение',
            'action_time': 130,
            'is_public': True,
        }
        response = self.client.post(reverse('habits:habit_create'), data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(),
                         {
                             "non_field_errors": [
                                 "Время выполнения привычки не должно быть больше 120 секунд",
                                 "У приятной привычки не может быть вознаграждения или связанной привычки"
                             ]
                         })

    def tearDown(self):
        pass
