from rest_framework import serializers
from .models import CycleTracking, Profile, GoalSetting

class CycleTrackingSerializer(serializers.ModelSerializer):
    class Meta:
        model=CycleTracking
        fields='__all__'

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model= GoalSetting
        fields='__all__'