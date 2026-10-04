from django.db import models
from django.conf import settings
from django.utils import timezone


class JobPosting(models.Model):
    """
    Job and contract opportunities for developers and designers.
    """
    LOCATION_TYPE_CHOICES = [
        ('remote', 'Uzaktan (Remote)'),
        ('hybrid', 'Hibrit (Hybrid)'),
        ('office', 'Ofis / Yerinde (On-site)'),
    ]

    JOB_TYPE_CHOICES = [
        ('full_time', 'Tam Zamanlı'),
        ('part_time', 'Yarı Zamanlı'),
        ('contract', 'Sözleşmeli / Freelance'),
        ('internship', 'Stajyer'),
    ]

    title = models.CharField(max_length=200, verbose_name="İlan Başlığı")
    company_name = models.CharField(max_length=150, verbose_name="Şirket / Kişi Adı")
    company_logo = models.ImageField(
        upload_to='jobs/',
        blank=True,
        null=True,
        verbose_name="Şirket Logosu"
    )
    location_type = models.CharField(
        max_length=20,
        choices=LOCATION_TYPE_CHOICES,
        default='remote',
        verbose_name="Çalışma Modeli"
    )
    location = models.CharField(
        max_length=120,
        blank=True,
        verbose_name="Lokasyon / Şehir",
        help_text="Örn: İstanbul, Berlin veya 'Dünya Geneli'"
    )
    job_type = models.CharField(
        max_length=20,
        choices=JOB_TYPE_CHOICES,
        default='full_time',
        verbose_name="İstihdam Türü"
    )
    description = models.TextField(
        verbose_name="İş ve Rol Tanımı",
        help_text="Aranan nitelikler, sorumluluklar ve teklif edilen yan haklar."
    )
    salary_range = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Bütçe / Maaş Skalası",
        help_text="Örn: 90.000 TL - 130.000 TL / Ay veya $4,000 - $6,000"
    )
    apply_url = models.CharField(
        max_length=255,
        verbose_name="Başvuru Linki veya E-posta",
        help_text="Örn: https://sirketiniz.com/kariyer veya mailto:hr@sirket.com"
    )
    deadline = models.DateField(
        blank=True,
        null=True,
        verbose_name="Son Başvuru Tarihi"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="İlan Aktif mi?"
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='job_postings',
        verbose_name="İlan Sahibi"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Son Güncelleme")

    class Meta:
        verbose_name = "İş İlanı"
        verbose_name_plural = "İş İlanları"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} @ {self.company_name}"

    @property
    def is_expired(self):
        if self.deadline:
            return self.deadline < timezone.now().date()
        return False
