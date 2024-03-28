from rest_framework import generics

# Create your views here.
from habits.models import Habit
from habits.serializers import HabitSerializer


class HabitCreateAPIView(generics.CreateAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer


class HabitListAPIView(generics.ListAPIView):
    serializer_class = HabitSerializer

    def get_queryset(self):
        return Habit.objects.filter(is_public=True)


class HabitRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = HabitSerializer

    def get_queryset(self):
        return Habit.objects.filter(is_public=True)
