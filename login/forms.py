from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import DanhGia, Group, User

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'mssv', 'classname', 'avatar', 'fullname')

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['classname', 'mssv', 'avatar', 'fullname']
        labels = {
            'classname': 'Class Name',
            'mssv': 'MSSV',
            'avatar': 'Profile Image',
            'fullname': 'Full Name'
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
class EvaluationForm(forms.ModelForm):
    number_choices = [(str(i), str(i)) for i in range(1, 6)]
    typedanhgia = forms.ChoiceField(choices=number_choices)
    score1 = forms.IntegerField(
        widget=forms.NumberInput(attrs={'type': 'range', 'min': 0, 'max': 10})
    )
    score2 = forms.IntegerField(
        widget=forms.NumberInput(attrs={'type': 'range', 'min': 0, 'max': 10})
    )
    score3 = forms.IntegerField(
        widget=forms.NumberInput(attrs={'type': 'range', 'min': 0, 'max': 10})
    )
    class Meta:
        model = DanhGia
        fields = ['title','typedanhgia', 'danhgia', 'score1','score2','score3']