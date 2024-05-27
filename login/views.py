from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

from .models import DanhGia, Group, User
from .forms import CustomUserCreationForm, CustomAuthenticationForm, EvaluationForm, GroupCreationForm, ProfileUpdateForm

def update_comma_separated_field(field, value, remove=False):
    if not field:
        return '' if remove else str(value)
    field_list = field.split(',')
    if remove:
        if str(value) in field_list:
            field_list.remove(str(value))
    else:
        if str(value) not in field_list:
            field_list.append(str(value))
    return ','.join(field_list)

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def home_view(request):
    user = request.user
    following_user_ids = user.following_user_id.split(',') if user.following_user_id else []
    followed_user_ids = user.followed_user_id.split(',') if user.followed_user_id else []
    accessible_group_ids = set(following_user_ids + followed_user_ids)

    groups = Group.objects.filter(id__in=accessible_group_ids)
    if request.method == 'POST':
        form = GroupCreationForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)  # Assuming the user is the one creating the group
            group.followed_user_id = None
            group.following_user_id = None  # Adjust as per your requirements
            group.save()
            group.followed_user_id = group.id
            group.save()
            request.user.followed_user_id = update_comma_separated_field(request.user.followed_user_id, group.id)
            request.user.following_user_id = update_comma_separated_field(request.user.following_user_id, group.id)
            request.user.save()
            return redirect('group', group_id=group.id)
    else:
        form = GroupCreationForm()
    return render(request, 'home.html', {'form': form, 'groups': groups})

@login_required
def group_view(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    user = request.user
    user_following_groups = user.following_user_id.split(',') if user.following_user_id else []
    user_followed_groups = user.followed_user_id.split(',') if user.followed_user_id else []
    if str(group_id) not in user_following_groups and str(group_id) not in user_followed_groups:
        messages.error(request, "Bạn không phải là một thành viên của nhóm này.")
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        action = request.POST.get('action')
        if 'delete_group' in request.POST:
            users = User.objects.all()
            for user in users:
                user.following_user_ids = update_comma_separated_field(user.following_user_id, group_id, remove=True)
                user.followed_user_ids = update_comma_separated_field(user.followed_user_id, group_id, remove=True)
                user.save()
            group.delete()
            messages.success(request, "The group has been deleted.")
            return redirect('home')
        try:
            user = User.objects.get(username=username)
            if action == 'add':
                user.following_user_id = update_comma_separated_field(user.following_user_id, group_id)
                messages.success(request, f"Đã thêm {username} vào trong nhóm.")
            elif action == 'remove':
                user.following_user_id = update_comma_separated_field(user.following_user_id, group_id, remove=True)
                messages.success(request, f"Đã thêm {username} vào trong nhóm.")
            user.save()
        except User.DoesNotExist:
            messages.error(request, "Người dùng không tồn tại.")
    members = User.objects.filter(following_user_id__icontains=str(group_id))
    return render(request, 'group.html', {'group': group, 'members':members})

@login_required
def profile_view(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, 'profile.html', {'form': form})

@login_required
def evaluate_member_view(request, group_id, member_id):
    group = get_object_or_404(Group, id=group_id)
    member = get_object_or_404(User, id=member_id)
    user = request.user
    user_following_groups = user.following_user_id.split(',') if user.following_user_id else []
    user_followed_groups = user.followed_user_id.split(',') if user.followed_user_id else []
    if str(group_id) not in user_following_groups and str(group_id) not in user_followed_groups:
        messages.error(request, "Bạn không phải là một thành viên của nhóm này.")
        return redirect('home')
    if request.method == 'POST':
        form = EvaluationForm(request.POST)
        if form.is_valid():
            score1 = form.cleaned_data['score1']
            score2 = form.cleaned_data['score2']
            score3 = form.cleaned_data['score3']
            average_score = (score1 + score2 + score3) / 3
            evaluation = form.save(commit=False)
            evaluation.groupid = group.id
            evaluation.user_id = member.id
            evaluation.score = average_score
            evaluation.nguoidanhgia = member.fullname
            evaluation.save()
            messages.success(request, f"Evaluation for {member.username} has been submitted.")
            return redirect('group', group_id)
        else:
            print(form.errors)  # Debug: Print form errors to the console
    else:
        form = EvaluationForm()

    return render(request, 'danhgia.html', {'group': group, 'member': member, 'form': form})

@login_required
def user_evaluations_view(request):
    user = request.user
    evaluations = DanhGia.objects.filter(user_id=user.id)
    return render(request, 'nhom.html', {'evaluations': evaluations})

@login_required
def group_summary_view(request,group_id):
    group = get_object_or_404(Group, id=group_id)
    evaluations = DanhGia.objects.filter(groupid=group_id)
    return render(request, 'groupdanhgia.html', {'group': group, 'evaluations': evaluations})