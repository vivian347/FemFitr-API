from django.db import models
from django.contrib.auth.models import User
from datetime import date
from recurrence.fields import RecurrenceField

# Create your models here.
class CycleTracking(models.Model):
    """take in fields required to track the users cycle"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    cycle_length = models.PositiveIntegerField()
    last_menstruation_start = models.DateField()
    tracked_date = models.DateField(auto_now_add=True)
    menstrual_events = RecurrenceField(default='')

    def age(self):
        today = date.today
        age = today.year - self.date_of_birth.year
        if today.month < self.date_of_birth.month or (today.month == self.date_of_birth.month and today.day < self.date_of_birth.day):
            age -= 1;
        return age
    def __str__(self):
        return f"Cycle Tracking for {self.user.username}"
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    height = models.FloatField()
    weight = models.FloatField()
    fitness_level = models.CharField(max_length=255)
    age = models.IntegerField()
    last_menstruation_start_date = models.DateField()
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    def __str__(self):
        return self.user.username
    
class GoalSetting(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    goal = models.CharField(max_length=255)
    description = models.TextField()
    target_date = models.DateField()
    is_completed = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.goal
    
class Exercise(models.Model):
    name = models.CharField(max_length=255)
    muscle = models.CharField(max_length=255)
    difficulty = models.CharField(max_length=255)
    equipment = models.CharField(max_length=255)
    description = models.CharField(max_length=10000)

    def __str__(self):
        return self.name
