from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q

from .models import JobPosting
from .forms import JobPostingForm


def job_list_view(request):
    """
    List and filter active job opportunities for developers and designers.
    """
    query = request.GET.get('q', '').strip()
    location_type = request.GET.get('location_type', '').strip()
    job_type = request.GET.get('job_type', '').strip()

    jobs = JobPosting.objects.filter(is_active=True).select_related('author')

    # Search filter
    if query:
        jobs = jobs.filter(
            Q(title__icontains=query) |
            Q(company_name__icontains=query) |
            Q(description__icontains=query) |
            Q(location__icontains=query)
        )

    # Location type filter (remote, hybrid, office)
    if location_type:
        jobs = jobs.filter(location_type=location_type)

    # Job type filter (full_time, part_time, contract, internship)
    if job_type:
        jobs = jobs.filter(job_type=job_type)

    # Paginate: 10 jobs per page
    paginator = Paginator(jobs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'jobs': page_obj.object_list,
        'query': query,
        'selected_location_type': location_type,
        'selected_job_type': job_type,
        'location_type_choices': JobPosting.LOCATION_TYPE_CHOICES,
        'job_type_choices': JobPosting.JOB_TYPE_CHOICES,
        'total_jobs': jobs.count(),
    }
    return render(request, 'jobs/list.html', context)


def job_detail_view(request, pk):
    """
    Display full details of a job posting.
    """
    job = get_object_or_404(JobPosting.objects.select_related('author'), pk=pk)

    # Check if visitor is the author of this posting
    is_owner = request.user.is_authenticated and request.user == job.author

    # Related or recent other jobs
    other_jobs = JobPosting.objects.filter(is_active=True).exclude(pk=job.pk)[:3]

    context = {
        'job': job,
        'is_owner': is_owner,
        'other_jobs': other_jobs,
    }
    return render(request, 'jobs/detail.html', context)


@login_required
def job_create_view(request):
    """
    Allow authenticated members to publish a new job opening.
    """
    if request.method == 'POST':
        form = JobPostingForm(request.POST, request.FILES)
        if form.is_valid():
            job = form.save(commit=False)
            job.author = request.user
            job.save()
            messages.success(request, f"'{job.title}' ilanı başarıyla yayınlandı!")
            return redirect('jobs:detail', pk=job.pk)
        else:
            messages.error(request, "İlan oluşturulamadı. Lütfen hataları kontrol edin.")
    else:
        form = JobPostingForm()

    return render(request, 'jobs/form.html', {
        'form': form,
        'title': 'Yeni İş İlanı Yayınla',
        'button_text': 'İlanı Yayınla',
        'is_edit': False
    })


@login_required
def job_update_view(request, pk):
    """
    Allow job author to update their job posting.
    """
    job = get_object_or_404(JobPosting, pk=pk)

    if job.author != request.user:
        messages.error(request, "Bu ilanı düzenleme yetkiniz bulunmuyor.")
        return redirect('jobs:detail', pk=job.pk)

    if request.method == 'POST':
        form = JobPostingForm(request.POST, request.FILES, instance=job)
        if form.is_valid():
            job = form.save()
            messages.success(request, "İlan başarıyla güncellendi!")
            return redirect('jobs:detail', pk=job.pk)
        else:
            messages.error(request, "Güncelleme sırasında bir hata oluştu.")
    else:
        form = JobPostingForm(instance=job)

    return render(request, 'jobs/form.html', {
        'form': form,
        'title': 'İlanı Düzenle',
        'button_text': 'Değişiklikleri Kaydet',
        'job': job,
        'is_edit': True
    })


@login_required
def job_delete_view(request, pk):
    """
    Allow job author to delete their job posting.
    """
    job = get_object_or_404(JobPosting, pk=pk)

    if job.author != request.user:
        messages.error(request, "Bu ilanı silme yetkiniz bulunmuyor.")
        return redirect('jobs:detail', pk=job.pk)

    if request.method == 'POST':
        title = job.title
        job.delete()
        messages.success(request, f"'{title}' ilanı başarıyla kaldırıldı.")
        return redirect('jobs:list')

    return render(request, 'jobs/confirm_delete.html', {'job': job})
