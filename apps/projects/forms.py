from django import forms
from .models import Project, Comment


class ProjectForm(forms.ModelForm):
    """
    Form to create or update a project showcase.
    """
    tags_raw = forms.CharField(
        label="Kullanılan Teknolojiler / Etiketler",
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Django, Vue.js, PostgreSQL, TailwindCSS, Redis (Virgülle ayırın)',
            'class': 'w-full px-4 py-2.5 bg-slate-800 border border-slate-700 rounded-lg text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition duration-200'
        }),
        help_text="Kullandığınız kütüphane, framework ve dilleri virgülle ayırarak girin."
    )

    class Meta:
        model = Project
        fields = [
            'title', 'category', 'cover_image',
            'demo_url', 'github_url', 'description'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Örn: DevConnect - Geliştirici Portfolyo & Ağ Platformu',
                'class': 'w-full px-4 py-2.5 bg-slate-800 border border-slate-700 rounded-lg text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition duration-200'
            }),
            'category': forms.Select(attrs={
                'class': 'w-full px-4 py-2.5 bg-slate-800 border border-slate-700 rounded-lg text-slate-100 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition duration-200'
            }),
            'cover_image': forms.FileInput(attrs={
                'class': 'block w-full text-sm text-slate-400 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-medium file:bg-indigo-600 file:text-white hover:file:bg-indigo-500 cursor-pointer'
            }),
            'demo_url': forms.URLInput(attrs={
                'placeholder': 'https://proje-canli-demo.com',
                'class': 'w-full px-4 py-2.5 bg-slate-800 border border-slate-700 rounded-lg text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition duration-200'
            }),
            'github_url': forms.URLInput(attrs={
                'placeholder': 'https://github.com/kullanici/proje-adi',
                'class': 'w-full px-4 py-2.5 bg-slate-800 border border-slate-700 rounded-lg text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition duration-200'
            }),
            'description': forms.Textarea(attrs={
                'rows': 8,
                'placeholder': '### Proje Hakkında\n\nBu proje ne işe yarıyor? Hangi problemleri çözüyor?\n\n### Mimari & Özellikler\n- REST API desteği\n- Docker ile konteynerizasyon\n- Dark mode arayüz...',
                'class': 'w-full font-mono text-sm px-4 py-2.5 bg-slate-800 border border-slate-700 rounded-lg text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition duration-200'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['tags_raw'].initial = self.instance.tags_as_string()

    def clean_tags_raw(self):
        raw = self.cleaned_data.get('tags_raw', '')
        if raw:
            return [t.strip() for t in raw.split(',') if t.strip()]
        return []

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.tags = self.cleaned_data.get('tags_raw', [])
        if commit:
            instance.save()
        return instance


class CommentForm(forms.ModelForm):
    """
    Form to post comments on a project.
    """
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Bu proje hakkında bir soru sorun, yapıcı geri bildirim verin veya düşüncelerinizi paylaşın...',
                'class': 'w-full px-4 py-2.5 bg-slate-800 border border-slate-700 rounded-lg text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition duration-200 resize-none'
            }),
        }
        labels = {
            'content': ''
        }
