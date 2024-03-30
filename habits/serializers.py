from rest_framework import serializers

from habits.models import Habit
from habits.validators import RewardAndHabitValidator, ActionTimeValidator, IsNiceValidator, NiceHabitValidator, PeriodValidator


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = '__all__'

        validators = [
            RewardAndHabitValidator(reward='reward', habit='associated_hab'),
            ActionTimeValidator(time='action_time'),
            IsNiceValidator(habit='associated_hab'),
            NiceHabitValidator(habit_is_nice='is_nice', reward='reward', habit='associated_hab'),
            PeriodValidator(period='period')
        ]
