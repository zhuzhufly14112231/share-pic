from django.shortcuts import render, HttpResponse, get_object_or_404
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
# Create your views here.
from account.forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from account.models import Profile, Content
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from action.utils import create_action
from action.models import Action


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'],
                                password=cd['password'])
            if user is None:
                return HttpResponse('登录失败')
            elif user .is_active:
                login(request, user)
                return HttpResponse('登录验证成功')
            else:
                return HttpResponse('You have been banned from Administrators')

    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form':form})


@login_required
def dashboard(request):
    # 默认展示所有行为,不包含当前用户
    actions = Action.objects.all()
    # 关注的用户的id列表
    following = Content.objects.filter(user_form=request.user)
    following_ids = [user_to.id for user_to in following]
    if following_ids:
        # 如果当前用户有关注的用户,仅展示被关注用户的行为
        actions = actions.filter(user_id__in=following_ids)
    actions = actions[:10]
    return render(request, 'account/dashboard.html', {'section': 'dashboard','actions':actions})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # 建立新数据对象但是不写入数据库
            new_user = user_form.save(commit=False)
            # 设置密码
            new_user.set_password(user_form.cleaned_data['password'])
            # 保存user对象
            new_user.save()
            Profile.objects.create(user=new_user)
            create_action(new_user,'创建了新用户')
            return render(request, 'account/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form': user_form})


@login_required
def edit(request):
    if request.method == 'POST':
        # instance 指定对象是数据库中的当前登录用户的哪一行数据对象,
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, '个人信息修改成功')
        else:
            messages.error(request, '个人信息修改失败')

    else:
        user_form = UserEditForm()
        profile_form = ProfileEditForm()
    return render(request, 'account/edit.html', {'user_form': user_form, 'profile_form': profile_form})


@login_required
def user_list(request):
    users = User.objects.filter(is_active=True)
    return render(request, 'account/user_list.html', {'users': users, 'section': 'users'})


@login_required
def user_detail(request, username):
    user = get_object_or_404(User, username=username, is_active=True)
    contents = Content.objects.filter(user_to=user)
    followers = [follower.user_form for follower in contents]
    total_followers = len(followers)
    return render(request, 'account/user_detail.html', {'user': user, 'section': 'users',
                                                        'followers': followers,
                                                        'total_followers': total_followers})

@login_required
@require_POST
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        user = User.objects.get(id=user_id)
        if action == 'follow':
            Content.objects.get_or_create(user_form=request.user,user_to=user)
            create_action(request.user,'关注了用户',user)
        else:
            Content.objects.filter(user_form=request.user,user_to=user).delete()
        return JsonResponse({'status':'ok'})
    return JsonResponse({'status':'error'})
