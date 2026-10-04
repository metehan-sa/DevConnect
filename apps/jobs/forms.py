from django import forms
from .models import JobPosting


class JobPostingForm(forms.ModelForm):
    """
    Form to create and edit job postings.
    """
    class Meta:
        model = JobPosting
        fields = [
            'title', 'company_name', 'company_logo',
            'location_type', 'location', 'job_type',
            'salary_range', 'apply_url', 'deadline',
            'description', 'is_active'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Örn: Senior Full-Stack Python / Django Developer',
                'class': 'w-full px-4 py-2.5 bg-slate-800 border border-slate-700 rounded-lg text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition duration-200'
            }),
            'company_name': forms.TextInput(attrs={
                'placeholder': 'Örn: Nexus Tech Labs',
                'class': 'w-full px-4 py-2.5 bg-slate-800 border border-slate-700 rounded-lg text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition duration-200'
            }),
            'company_logo': forms.FileInput(attrs={
                'class': 'block w-full text-sm text-slate-400 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-medium file:bg-indigo-600 file:text-white hover:file:bg-indigo-500 cursor-pointer'
            }),
            'location_type': forms.Select(attrs={
                'class': 'w-full px-4 py-2.5 bg-slate-800 border border-slate-700 rounded-lg text-slate-100 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition duration-200'
            }),
            'location': forms.TextInput(attrs={
                'placeholder': 'Örn: İstanbul (Hibrit) veya Dünya Çapı',
                'class': 'w-full px-4 py-2.5 bg-slate-800 border border-slate-700 rounded-lg text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition duration-200'
            }),
            'job_type': forms.Select(attrs={
                'class': 'w-full px-4 py-2.5 bg-slate-800 border border-slate-700 rounded-lg text-slate-100 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition duration-200'
            }),
            'salary_range': forms.TextInput(attrs={
                'placeholder': 'Örn: 90.000 TL - 120.000 TL / Ay veya $4,000 - $6,000',
                'class': 'w-full px-4 py-2.5 bg-slate-800 border border-slate-700 rounded-lg text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition duration-200'
            }),
            'apply_url': forms.TextInput(attrs={
                'placeholder': 'https://kariyer.sirket.com veya mailto:jobs@sirket.com',
                'class': 'w-full px-4 py-2.5 bg-slate-800 border border-slate-700 rounded-lg text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition duration-200'
            }),
            'deadline': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full px-4 py-2.5 bg-slate-800 border border-slate-700 rounded-lg text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition duration-200'
            }),
            'description': forms.Textarea(attrs={
                'rows': 7,
                'placeholder': 'İlan detayları, teknik gereksinimler, şirket kültürü ve başvuru sürecini yazın...',
                'class': 'w-full px-4 py-2.5 bg-slate-800 border border-slate-700 rounded-lg text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition duration-200'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'w-5 h-5 text-indigo-600 bg-slate-800 border-slate-700 rounded focus:ring-indigo-500'
            }),
        }
