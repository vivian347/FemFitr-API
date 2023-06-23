from django.urls import path
from . import views
from allauth.account.views import LoginView, SignupView, LogoutView, ConfirmEmailView

urlpatterns = [
    path('', views.home, name="view_name"),
    path('login/', LoginView.as_view(), name='account_login'),
    path('signup/', SignupView.as_view(), name='account_signup'),
    path('logout/', LogoutView.as_view(), name='account_logout'),
    path('cycle-track/', views.cycle_tracking_view),
    path('profile/', views.get_profile_all, name='profiles'),
    path('profile/<int:user_id>/', views.get_profile, name='user-profile'),
    path('create-profile/', views.create_profile, name='create-profile'),
    path('update-profile/<int:user_id>/', views.update_profile, name='update-profile'),
    path('set-goal/<int:user_id>/', views.set_goal, name='set-goal'),
    path('goals/<int:user_id>/', views.get_user_goals, name='goals'),
    path('user-goal/<int:user_id>/<int:goal_id>/', views.get_goal, name='user-goal'),
    path('update-goal/<int:user_id>/<int:goal_id>/', views.update_goal, name='update-goal'),
    path('delete-goal/<int:user_id>/<int:goal_id>/', views.delete_goal, name='delete-goal')
]
