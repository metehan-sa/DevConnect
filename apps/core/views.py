from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.db.models import Count

from apps.projects.models import Project
from apps.jobs.models import JobPosting

User = get_user_model()


def home_view(request):
    """
    Landing page showcasing featured projects, latest jobs, and live platform metrics.
    """
    # Featured Projects (ordered by total likes or newest)
    featured_projects = (
        Project.objects.all()
        .select_related('author', 'author__profile')
        .prefetch_related('likes', 'comments')
        .annotate(num_likes=Count('likes'))
        .order_by('-num_likes', '-created_at')[:6]
    )

    # Latest Active Job Postings
    latest_jobs = (
        JobPosting.objects.filter(is_active=True)
        .select_related('author')
        .order_by('-created_at')[:4]
    )

    # Platform Statistics
    total_developers = User.objects.count()
    total_projects = Project.objects.count()
    total_jobs = JobPosting.objects.filter(is_active=True).count()
    
    # Calculate total community likes
    total_likes = sum(p.likes.count() for p in Project.objects.all())

    context = {
        'featured_projects': featured_projects,
        'latest_jobs': latest_jobs,
        'stats': {
            'developers': total_developers,
            'projects': total_projects,
            'jobs': total_jobs,
            'likes': total_likes,
        },
        'categories': Project.CATEGORY_CHOICES,
    }
    return render(request, 'core/home.html', context)
