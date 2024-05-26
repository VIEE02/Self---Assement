from django.urls import path
from .views import group_view, home_view, register_view, login_view, logout_view ,profile_view

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('home/', home_view, name='home'),
    path('profile/', profile_view, name='profile'),
    path('group/<int:group_id>/', group_view, name='group'),
]