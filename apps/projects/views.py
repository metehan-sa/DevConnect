from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.http import require_POST

from .models import Project, Comment
from .forms import ProjectForm, CommentForm


def project_list_view(request):
    """
    Searchable, filterable and paginated list of projects.
    """
    query = request.GET.get('q', '').strip()
    category = request.GET.get('category', '').strip()
    tag = request.GET.get('tag', '').strip()
    sort = request.GET.get('sort', 'newest')

    projects = (
        Project.objects.all()
        .select_related('author', 'author__profile')
        .prefetch_related('likes', 'comments')
    )

    # Search filter
    if query:
        projects = projects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(author__username__icontains=query) |
            Q(author__first_name__icontains=query) |
            Q(author__last_name__icontains=query)
        )

    # Category filter
    if category:
        projects = projects.filter(category=category)

    # Tag filter
    if tag:
        projects = projects.filter(tags__contains=[tag])

    # Sorting
    if sort == 'likes':
        projects = projects.annotate(num_likes=Count('likes')).order_by('-num_likes', '-created_at')
    elif sort == 'views':
        projects = projects.order_by('-views_count', '-created_at')
    elif sort == 'oldest':
        projects = projects.order_by('created_at')
    else:
        # Default newest
        projects = projects.order_by('-created_at')

    # Pagination: 9 projects per page
    paginator = Paginator(projects, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Project.CATEGORY_CHOICES

    context = {
        'page_obj': page_obj,
        'projects': page_obj.object_list,
        'query': query,
        'selected_category': category,
        'selected_tag': tag,
        'selected_sort': sort,
        'categories': categories,
        'total_results': projects.count(),
    }
    return render(request, 'projects/list.html', context)


def project_detail_view(request, slug):
    """
    Show full details of a project, render markdown, track views, display comments & likes.
    """
    project = get_object_or_404(
        Project.objects.select_related('author', 'author__profile').prefetch_related('likes'),
        slug=slug
    )

    # Session-based view counting to prevent refresh spam
    session_key = f'viewed_project_{project.id}'
    if not request.session.get(session_key, False):
        Project.objects.filter(pk=project.pk).update(views_count=project.views_count + 1)
        project.views_count += 1
        request.session[session_key] = True

    comments = (
        project.comments.all()
        .select_related('author', 'author__profile')
        .order_by('created_at')
    )
    comment_form = CommentForm()

    user_has_liked = False
    if request.user.is_authenticated:
        user_has_liked = project.likes.filter(id=request.user.id).exists()

    # More projects by the same author
    related_projects = (
        Project.objects.filter(author=project.author)
        .exclude(pk=project.pk)[:3]
    )

    context = {
        'project': project,
        'comments': comments,
        'comment_form': comment_form,
        'user_has_liked': user_has_liked,
        'related_projects': related_projects,
    }
    return render(request, 'projects/detail.html', context)


@login_required
def project_create_view(request):
    """
    Allow authenticated developers to create and publish a project showcase.
    """
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.author = request.user
            project.save()
            messages.success(request, f"'{project.title}' projeniz başarıyla yayınlandı!")
            return redirect('projects:detail', slug=project.slug)
        else:
            messages.error(request, "Proje kaydedilemedi. Lütfen formu kontrol edin.")
    else:
        form = ProjectForm()

    return render(request, 'projects/form.html', {
        'form': form,
        'title': 'Yeni Proje Yayınla',
        'button_text': 'Projeyi Yayınla',
        'is_edit': False
    })


@login_required
def project_update_view(request, slug):
    """
    Allow the project author to update project information.
    """
    project = get_object_or_404(Project, slug=slug)

    if project.author != request.user:
        messages.error(request, "Bu projeyi düzenleme yetkiniz bulunmuyor.")
        return redirect('projects:detail', slug=project.slug)

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            project = form.save()
            messages.success(request, "Projeniz başarıyla güncellendi!")
            return redirect('projects:detail', slug=project.slug)
        else:
            messages.error(request, "Güncelleme sırasında hata oluştu.")
    else:
        form = ProjectForm(instance=project)

    return render(request, 'projects/form.html', {
        'form': form,
        'title': 'Projeyi Düzenle',
        'button_text': 'Değişiklikleri Kaydet',
        'project': project,
        'is_edit': True
    })


@login_required
def project_delete_view(request, slug):
    """
    Allow the project author to delete their project with confirmation.
    """
    project = get_object_or_404(Project, slug=slug)

    if project.author != request.user:
        messages.error(request, "Bu projeyi silme yetkiniz bulunmuyor.")
        return redirect('projects:detail', slug=project.slug)

    if request.method == 'POST':
        title = project.title
        project.delete()
        messages.success(request, f"'{title}' projesi başarıyla silindi.")
        return redirect('accounts:profile', username=request.user.username)

    return render(request, 'projects/confirm_delete.html', {'project': project})


@login_required
@require_POST
def project_toggle_like(request, slug):
    """
    Toggle like on a project. Supports AJAX response and standard POST redirect.
    """
    project = get_object_or_404(Project, slug=slug)
    user = request.user

    if project.likes.filter(id=user.id).exists():
        project.likes.remove(user)
        liked = False
    else:
        project.likes.add(user)
        liked = True

    total_likes = project.likes.count()

    # Check if AJAX request
    is_ajax = (
        request.headers.get('x-requested-with') == 'XMLHttpRequest' or
        request.headers.get('accept') == 'application/json'
    )
    if is_ajax:
        return JsonResponse({
            'liked': liked,
            'total_likes': total_likes
        })

    return redirect('projects:detail', slug=slug)


@login_required
@require_POST
def project_add_comment(request, slug):
    """
    Add a comment to a project.
    """
    project = get_object_or_404(Project, slug=slug)
    form = CommentForm(request.POST)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.project = project
        comment.author = request.user
        comment.save()
        messages.success(request, "Yorumunuz başarıyla eklendi.")
    else:
        messages.error(request, "Yorum eklenirken bir hata oluştu.")

    return redirect('projects:detail', slug=slug)
