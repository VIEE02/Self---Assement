from django.urls import path
from .views import evaluate_member_view, group_summary_view, group_view, home_view, register_view, login_view, logout_view ,profile_view, user_evaluations_view

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('home/', home_view, name='home'),
    path('profile/', profile_view, name='profile'),
    path('group/<int:group_id>/', group_view, name='group'),
    path('group/<int:group_id>/evaluate/<int:member_id>/', evaluate_member_view, name='evaluate_member'),
    path('evaluations/', user_evaluations_view, name='user_evaluations'),
    path('group/<int:group_id>/summary/', group_summary_view, name='group_summary'),
]