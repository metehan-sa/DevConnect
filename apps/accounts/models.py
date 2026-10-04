from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
import urllib.parse


class User(AbstractUser):
    """
    Custom User model extending AbstractUser.
    Using unique email for modern authentication standards.
    """
    email = models.EmailField(unique=True, verbose_name="E-posta Adresi")

    class Meta:
        verbose_name = "Kullanıcı"
        verbose_name_plural = "Kullanıcılar"
        ordering = ['-date_joined']

    def __str__(self):
        return self.username

    def get_display_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username


class UserProfile(models.Model):
    """
    Extended user profile for developers and designers on DevConnect.
    """
    SPECIALIZATION_CHOICES = [
        ('frontend', 'Frontend Geliştirici'),
        ('backend', 'Backend Geliştirici'),
        ('fullstack', 'Full Stack Geliştirici'),
        ('mobile', 'Mobil Uygulama Geliştirici'),
        ('uiux', 'UI/UX Tasarımcı'),
        ('devops', 'DevOps / Cloud Mühendisi'),
        ('data_ai', 'Veri Bilimi & Yapay Zeka'),
        ('other', 'Yazılım & Tasarım Uzmanı'),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name="Kullanıcı"
    )
    bio = models.TextField(
        max_length=600,
        blank=True,
        verbose_name="Biyografi",
        help_text="Kendinizi, ilgi alanlarınızı ve çalışma hedeflerinizi özetleyin."
    )
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        verbose_name="Profil Fotoğrafı"
    )
    specialization = models.CharField(
        max_length=30,
        choices=SPECIALIZATION_CHOICES,
        default='fullstack',
        verbose_name="Uzmanlık Alanı"
    )
    skills = models.JSONField(
        default=list,
        blank=True,
        verbose_name="Yetenekler (Skills)",
        help_text="Örnek: ['Python', 'Django', 'Tailwind CSS', 'React']"
    )
    github_url = models.URLField(
        max_length=250,
        blank=True,
        null=True,
        verbose_name="GitHub Profili"
    )
    linkedin_url = models.URLField(
        max_length=250,
        blank=True,
        null=True,
        verbose_name="LinkedIn Profili"
    )
    website_url = models.URLField(
        max_length=250,
        blank=True,
        null=True,
        verbose_name="Kişisel Web Sitesi / Portfolyo"
    )
    location = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Konum / Şehir"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Son Güncelleme")

    class Meta:
        verbose_name = "Kullanıcı Profili"
        verbose_name_plural = "Kullanıcı Profilleri"

    def __str__(self):
        return f"{self.user.username} Profili"

    @property
    def avatar_url(self):
        """
        Returns uploaded avatar URL or an aesthetic fallback avatar using Dicebear API.
        """
        if self.avatar and hasattr(self.avatar, 'url'):
            return self.avatar.url
        name_encoded = urllib.parse.quote(self.user.get_display_name())
        return f"https://api.dicebear.com/7.x/bottts/svg?seed={name_encoded}&backgroundColor=1e293b"

    def skills_as_string(self):
        """Returns comma-separated skills for forms."""
        if isinstance(self.skills, list):
            return ", ".join(self.skills)
        return ""
