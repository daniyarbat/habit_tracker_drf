from rest_framework.exceptions import ValidationError


class RewardAndHabitValidator:
    def __init__(self, reward, habit):
        self.reward = reward
        self.habit = habit

    def __call__(self, value):
        reward = dict(value).get(self.reward)
        habit = dict(value).get(self.habit)
        if reward and habit:
            raise ValidationError('Нельзя одновременно выбирать связанную привычку и вознаграждение')


class ActionTimeValidator:
    def __init__(self, time):
        self.time = time

    def __call__(self, value):
        time = dict(value).get(self.time)
        if time > 120:
            raise ValidationError('Время выполнения привычки не должно быть больше 120 секунд')


class IsNiceValidator:
    def __init__(self, habit):
        self.habit = habit

    def __call__(self, value):
        if value.get(self.habit):
            is_nice = dict(value).get(self.habit).is_nice
            if not is_nice:
                raise ValidationError('В связанные привычки могут попадать только привычки с признаком приятной привычки')


class NiceHabitValidator:
    def __init__(self, habit_is_nice, reward, habit):
        self.habit_is_nice = habit_is_nice
        self.reward = reward
        self.habit = habit

    def __call__(self, value):
        habit_is_nice = dict(value).get(self.habit_is_nice)
        reward = dict(value).get(self.reward)
        habit = dict(value).get(self.habit)
        if habit_is_nice:
            if reward or habit:
                raise ValidationError('У приятной привычки не может быть вознаграждения или связанной привычки')


class PeriodValidator:
    def __init__(self, period):
        self.period = period

    def __call__(self, value):
        period = dict(value).get(self.period)
        if period < 1:
            raise ValidationError('Нельзя выполнять привычку реже, чем 1 раз в 7 дней')
