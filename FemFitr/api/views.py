from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import CycleTracking, Profile, GoalSetting
from .serializers import CycleTrackingSerializer, ProfileSerializer, GoalSerializer
from datetime import datetime, timedelta
from recurrence import Recurrence, Rule
import recurrence
from django.shortcuts import get_object_or_404

# Create your views here.
api_view(['GET'])
def home(request):
    return render(request, 'home.html', {})
    
# View to collect data needed for cycle tracking
@api_view(['POST'])
def cycle_tracking_view(request):

    user = request.user
    dob = request.data.get('date_of_birth')
    cycle_length = request.data.get('cycle_length')
    last_menstruation_start = request.data.get('last_menstruation_start')

    if not last_menstruation_start:
        return Response({'error': 'Last menstruation start date is required.'}, status=400)

    date_of_birth = datetime.strptime(dob, '%Y-%m-%d').date()
    last_menstruation = datetime.strptime(last_menstruation_start, '%Y-%m-%d').date()
    
    menstrual_start_date = last_menstruation
    menstrual_end_date  = last_menstruation + timedelta(4)

    follicular_start_date = menstrual_start_date
    follicular_end_date = menstrual_start_date + timedelta(15)

    ovulation_date = menstrual_start_date + timedelta(days=16)

    luteal_start_date = ovulation_date + timedelta(days=1)
    luteal_end_date = ovulation_date + timedelta(cycle_length - 16)

    start_date = datetime.combine(menstrual_start_date, datetime.min.time())
    end_date = datetime.combine(luteal_end_date, datetime.max.time())

    rules = Rule(recurrence.MONTHLY, by_month_day=[last_menstruation.day])
    
    my_recurrence = Recurrence(
        rrules=[rules],
        dtstart=start_date,
        dtend=end_date
    )

    cycle_tracking = CycleTracking(
        user=user,
        date_of_birth=date_of_birth,
        last_menstruation_start=last_menstruation_start,
        cycle_length=cycle_length,
        menstrual_events=str(my_recurrence)
    )
    cycle_tracking.save()

    response_data = {
        'menstrual_start_date': menstrual_start_date,
        'menstrual_end_date': menstrual_end_date,
        'follicular_start_date': follicular_start_date,
        'follicular_end_date': follicular_end_date,
        'ovulation_date': ovulation_date,
        'luteal_start_date': luteal_start_date,
        'luteal_end_date': luteal_end_date
    }

    return Response(response_data, status=201)

@api_view(['GET'])
def get_profile_all(request, user_id=None):
    profiles = Profile.objects.all()
    serializer=ProfileSerializer(profiles, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_profile(request, user_id=None):
    profile = get_object_or_404(Profile, user=user_id)
    serializer=ProfileSerializer(profile)
    return Response(serializer.data)

@api_view(['POST'])
def create_profile(request):
    serializer = ProfileSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['PUT'])
def update_profile(request, user_id):
    try:
        profile = Profile.objects.get(user_id=user_id)
    except Profile.DoesNotExist:
        return Response({'error': 'Profile not found.'}, status=404)
    
    serializer = ProfileSerializer(profile, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=200)
    return Response(serializer.errors, status=400)

@api_view(['POST'])
def set_goal(request, user_id):
    profile = get_object_or_404(Profile, user_id=user_id)

    goal_data = {
        'user': profile.user.id,
        'goal': request.data.get('goal'),
        'description': request.data.get('description'),
        'target_date': request.data.get('target_date'),
    }

    serializer = GoalSerializer(data=goal_data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)

    return Response(serializer.errors, status=401)

@api_view(['GET'])
def get_user_goals(request, user_id):
    profile = get_object_or_404(Profile, user_id=user_id)
    goals = GoalSetting.objects.filter(user=profile.user)
    serializer = GoalSerializer(goals, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_goal(request, user_id, goal_id):
    profile = get_object_or_404(Profile, user_id=user_id)
    goal = get_object_or_404(GoalSetting, user=profile.id, id=goal_id)
    serializer = GoalSerializer(goal)
    return Response(serializer.data, status=200)


@api_view(['PUT'])
def update_goal(request, user_id, goal_id):
    profile = get_object_or_404(Profile, user_id=user_id)
    goal = get_object_or_404(GoalSetting, user=profile.id, id=goal_id)
    serializer = GoalSerializer(goal, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)

@api_view(['DELETE'])
def delete_goal(request, user_id, goal_id):
    profile = get_object_or_404(Profile, user_id=user_id)
    goal = get_object_or_404(GoalSetting, user=profile.user, id=goal_id)
    goal.delete()
    return Response(status=204)

