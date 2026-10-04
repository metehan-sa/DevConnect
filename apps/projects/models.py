from django.db import models
from django.conf import settings
from django.utils.text import slugify
import uuid


def turkish_slugify(text):
    """
    Generate clean URL slugs handling Turkish characters gracefully.
    """
    tr_map = {
        'ı': 'i', 'İ': 'i', 'ğ': 'g', 'Ğ': 'g',
        'ü': 'u', 'Ü': 'u', 'ş': 's', 'Ş': 's',
        'ö': 'o', 'Ö': 'o', 'ç': 'c', 'Ç': 'c'
    }
    for tr_char, en_char in tr_map.items():
        text = text.replace(tr_char, en_char)
    return slugify(text)


class Project(models.Model):
    """
    Project model for developers and designers to showcase work.
    """
    CATEGORY_CHOICES = [
        ('web', 'Web Geliştirme'),
        ('mobile', 'Mobil Uygulama'),
        ('uiux', 'UI / UX Tasarım'),
        ('ai', 'Yapay Zeka & Veri'),
        ('devops', 'DevOps & Bulut'),
        ('opensource', 'Açık Kaynak'),
        ('game', 'Oyun Geliştirme'),
        ('other', 'Diğer'),
    ]

    title = models.CharField(max_length=200, verbose_name="Proje Başlığı")
    slug = models.SlugField(max_length=260, unique=True, blank=True, verbose_name="URL Slug")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='projects',
        verbose_name="Geliştirici / Yazar"
    )
    category = models.CharField(
        max_length=30,
        choices=CATEGORY_CHOICES,
        default='web',
        verbose_name="Kategori"
    )
    description = models.TextField(
        verbose_name="Proje Açıklaması",
        help_text="Markdown formatı desteklenir. Projenin mimarisi, özellikleri ve kurulum adımlarını detaylandırın."
    )
    cover_image = models.ImageField(
        upload_to='projects/',
        blank=True,
        null=True,
        verbose_name="Kapak Görseli"
    )
    demo_url = models.URLField(
        blank=True,
        null=True,
        verbose_name="Canlı Demo URL'i",
        help_text="Örn: https://projem.com"
    )
    github_url = models.URLField(
        blank=True,
        null=True,
        verbose_name="GitHub Deposu (Repository)",
        help_text="Örn: https://github.com/kullanici/repo"
    )
    tags = models.JSONField(
        default=list,
        blank=True,
        verbose_name="Kullanılan Teknolojiler / Etiketler"
    )
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='liked_projects',
        blank=True,
        verbose_name="Beğeniler"
    )
    views_count = models.PositiveIntegerField(default=0, verbose_name="Görüntülenme Sayısı")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Son Güncelleme")

    class Meta:
        verbose_name = "Proje"
        verbose_name_plural = "Projeler"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def total_likes(self):
        return self.likes.count()

    def total_comments(self):
        return self.comments.count()

    @property
    def cover_url(self):
        """
        Returns uploaded cover image or high-quality developer placeholder.
        """
        if self.cover_image and hasattr(self.cover_image, 'url'):
            return self.cover_image.url
        # Modern aesthetic placeholder
        return "https://images.unsplash.com/photo-1555066931-4365d14bab8c?q=80&w=1200&auto=format&fit=crop"

    def tags_as_string(self):
        if isinstance(self.tags, list):
            return ", ".join(self.tags)
        return ""

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = turkish_slugify(self.title) or 'project'
            unique_slug = base_slug
            counter = 1
            while Project.objects.filter(slug=unique_slug).exclude(pk=self.pk).exists():
                unique_slug = f"{base_slug}-{uuid.uuid4().hex[:6]}"
                counter += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)


class Comment(models.Model):
    """
    Comments made on projects by community members.
    """
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name="Proje"
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='project_comments',
        verbose_name="Yazar"
    )
    content = models.TextField(verbose_name="Yorum")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Tarih")

    class Meta:
        verbose_name = "Yorum"
        verbose_name_plural = "Yorumlar"
        ordering = ['created_at']

    def __str__(self):
        return f"{self.author.username} - {self.project.title}"
