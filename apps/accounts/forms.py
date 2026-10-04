from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from .models import UserProfile

User = get_user_model()


class UserRegistrationForm(forms.ModelForm):
    """
    Form for registering a new user on DevConnect.
    """
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': '••••••••',
            'class': 'w-full px-4 py-2.5 bg-slate-800 border border-slate-700 rounded-lg text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition duration-200'
        }),
        label="Parola",
        min_length=8,
        help_text="En az 8 karakter uzunluğunda olmalıdır."
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': '••••••••',
            'class': 'w-full px-4 py-2.5 bg-slate-800 border border-slate-700 rounded-lg text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition duration-200'
        }),
        label="Parola Tekrarı"
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': 'kullanici_adi',
                'class': 'w-full px-4 py-2.5 bg-slate-800 border border-slate-700 rounded-lg text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition duration-200'
            }),
            'first_name': forms.TextInput(attrs={
                'placeholder': 'Adınız',
                'class': 'w-full px-4 py-2.5 bg-slate-800 border border-slate-700 rounded-lg text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition duration-200'
            }),
            'last_name': forms.TextInput(attrs={
                'placeholder': 'Soyadınız',
                'class': 'w-full px-4 py-2.5 bg-slate-800 border border-slate-700 rounded-lg text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition duration-200'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'ornek@devconnect.dev',
                'class': 'w-full px-4 py-2.5 bg-slate-800 border border-slate-700 rounded-lg text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition duration-200'
            }),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Bu e-posta adresiyle kayıtlı bir hesap zaten var.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', "Parolalar birbiriyle eşleşmiyor.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserLoginForm(AuthenticationForm):
    """
    Styled login form for DevConnect.
    """
    username = forms.CharField(
        label="Kullanıcı Adı",
        widget=forms.TextInput(attrs={
            'placeholder': 'kullanici_adi',
            'class': 'w-full px-4 py-2.5 bg-slate-800 border border-slate-700 rounded-lg text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition duration-200'
        })
    )
    password = forms.CharField(
        label="Parola",
        widget=forms.PasswordInput(attrs={
            'placeholder': '••••••••',
            'class': 'w-full px-4 py-2.5 bg-slate-800 border border-slate-700 rounded-lg text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition duration-200'
        })
    )


class UserUpdateForm(forms.ModelForm):
    """
    Form to update basic user identity info.
    """
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 bg-slate-800 border border-slate-700 rounded-lg text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition duration-200'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 bg-slate-800 border border-slate-700 rounded-lg text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition duration-200'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-2.5 bg-slate-800 border border-slate-700 rounded-lg text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition duration-200'
            }),
        }


class UserProfileUpdateForm(forms.ModelForm):
    """
    Form to update portfolio profile details.
    """
    skills_raw = forms.CharField(
        label="Yetenekler & Teknolojiler",
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Python, Django, Tailwind CSS, PostgreSQL, React (Virgülle ayırın)',
            'class': 'w-full px-4 py-2.5 bg-slate-800 border border-slate-700 rounded-lg text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition duration-200'
        }),
        help_text="Kullandığınız teknolojileri virgülle ayırarak yazın."
    )

    class Meta:
        model = UserProfile
        fields = [
            'bio', 'specialization', 'avatar',
            'github_url', 'linkedin_url', 'website_url', 'location'
        ]
        widgets = {
            'bio': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Kendinizi, kariyer hedeflerinizi ve üzerine çalıştığınız alanları tanıtın...',
                'class': 'w-full px-4 py-2.5 bg-slate-800 border border-slate-700 rounded-lg text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition duration-200'
            }),
            'specialization': forms.Select(attrs={
                'class': 'w-full px-4 py-2.5 bg-slate-800 border border-slate-700 rounded-lg text-slate-100 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition duration-200'
            }),
            'avatar': forms.FileInput(attrs={
                'class': 'block w-full text-sm text-slate-400 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-medium file:bg-indigo-600 file:text-white hover:file:bg-indigo-500 cursor-pointer'
            }),
            'github_url': forms.URLInput(attrs={
                'placeholder': 'https://github.com/kullaniciadi',
                'class': 'w-full px-4 py-2.5 bg-slate-800 border border-slate-700 rounded-lg text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition duration-200'
            }),
            'linkedin_url': forms.URLInput(attrs={
                'placeholder': 'https://linkedin.com/in/kullaniciadi',
                'class': 'w-full px-4 py-2.5 bg-slate-800 border border-slate-700 rounded-lg text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition duration-200'
            }),
            'website_url': forms.URLInput(attrs={
                'placeholder': 'https://portfolyonuz.com',
                'class': 'w-full px-4 py-2.5 bg-slate-800 border border-slate-700 rounded-lg text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition duration-200'
            }),
            'location': forms.TextInput(attrs={
                'placeholder': 'İstanbul, Türkiye / Uzaktan',
                'class': 'w-full px-4 py-2.5 bg-slate-800 border border-slate-700 rounded-lg text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition duration-200'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['skills_raw'].initial = self.instance.skills_as_string()

    def clean_skills_raw(self):
        raw_skills = self.cleaned_data.get('skills_raw', '')
        if raw_skills:
            # Clean and split skills by comma
            skills = [s.strip() for s in raw_skills.split(',') if s.strip()]
            return skills
        return []

    def save(self, commit=True):
        profile = super().save(commit=False)
        profile.skills = self.cleaned_data.get('skills_raw', [])
        if commit:
            profile.save()
        return profile
