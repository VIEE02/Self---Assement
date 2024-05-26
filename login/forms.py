from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Group, User

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'mssv', 'classname', 'avatar')

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['classname', 'mssv', 'avatar']
        labels = {
            'classname': 'Class Name',
            'mssv': 'MSSV',
            'avatar': 'Profile Image'
        }
class GroupCreationForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['groupname', 'following_user_id', 'followed_user_id']
        widgets = {
            'following_user_id': forms.HiddenInput(),
            'followed_user_id': forms.HiddenInput(),
        }
        labels = {
            'groupname': 'Group Name'
        }