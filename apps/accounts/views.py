from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count

from .forms import (
    UserRegistrationForm,
    UserLoginForm,
    UserUpdateForm,
    UserProfileUpdateForm
)
from apps.projects.models import Project

User = get_user_model()


def register_view(request):
    """
    Handle user registration with automated login upon success.
    """
    if request.user.is_authenticated:
        return redirect('core:home')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(
                request,
                f"DevConnect'e hoş geldiniz, @{user.username}! Profiliniz başarıyla oluşturuldu."
            )
            return redirect('accounts:edit_profile')
        else:
            messages.error(request, "Lütfen formdaki hataları düzeltin.")
    else:
        form = UserRegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    """
    Handle user login.
    """
    if request.user.is_authenticated:
        return redirect('core:home')

    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Tekrar hoş geldiniz, {user.get_display_name()}!")
            next_url = request.GET.get('next') or 'core:home'
            return redirect(next_url)
        else:
            messages.error(request, "Geçersiz kullanıcı adı veya parola.")
    else:
        form = UserLoginForm()

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    """
    Handle user logout for both GET and POST requests.
    """
    logout(request)
    messages.info(request, "Başarıyla çıkış yaptınız. Görüşmek üzere!")
    return redirect('core:home')


def profile_view(request, username):
    """
    Show public portfolio and developer profile of a user.
    """
    user_obj = get_object_or_404(User.objects.select_related('profile'), username=username)
    projects = (
        Project.objects.filter(author=user_obj)
        .prefetch_related('likes', 'comments')
        .order_by('-created_at')
    )

    # Statistics
    total_projects = projects.count()
    total_likes_received = sum(p.likes.count() for p in projects)

    context = {
        'profile_user': user_obj,
        'profile': getattr(user_obj, 'profile', None),
        'projects': projects,
        'total_projects': total_projects,
        'total_likes_received': total_likes_received,
        'is_own_profile': request.user.is_authenticated and request.user == user_obj,
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def edit_profile_view(request):
    """
    Allow authenticated user to edit their personal info and developer profile.
    """
    user = request.user
    profile = user.profile

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=user)
        p_form = UserProfileUpdateForm(request.POST, request.FILES, instance=profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Profil bilgileriniz başarıyla güncellendi!")
            return redirect('accounts:profile', username=user.username)
        else:
            messages.error(request, "Profil güncellenirken bir hata oluştu. Lütfen alanları kontrol edin.")
    else:
        u_form = UserUpdateForm(instance=user)
        p_form = UserProfileUpdateForm(instance=profile)

    return render(request, 'accounts/edit_profile.html', {
        'u_form': u_form,
        'p_form': p_form,
    })
