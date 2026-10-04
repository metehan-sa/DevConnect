from django.contrib import admin
from .models import JobPosting


@admin.register(JobPosting)
class JobPostingAdmin(admin.ModelAdmin):
    list_display = ('title', 'company_name', 'location_type', 'job_type', 'is_active', 'deadline', 'created_at')
    list_filter = ('location_type', 'job_type', 'is_active', 'created_at')
    search_fields = ('title', 'company_name', 'description', 'location')
    date_hierarchy = 'created_at'
