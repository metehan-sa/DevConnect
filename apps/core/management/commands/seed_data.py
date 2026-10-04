from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.projects.models import Project, Comment
from apps.jobs.models import JobPosting
from datetime import date, timedelta

User = get_user_model()


class Command(BaseCommand):
    help = "DevConnect için zengin demo verileri (kullanıcılar, projeler, ilanlar) oluşturur."

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.NOTICE("Demo verileri oluşturuluyor..."))

        # 1. Admin Kullanıcısı
        admin_user, _ = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@devconnect.dev',
                'first_name': 'DevConnect',
                'last_name': 'Yöneticisi',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        admin_user.set_password('admin123')
        admin_user.save()
        if hasattr(admin_user, 'profile'):
            admin_user.profile.bio = "DevConnect platform mimarı ve sistem yöneticisi."
            admin_user.profile.specialization = "fullstack"
            admin_user.profile.skills = ["Python", "Django", "PostgreSQL", "Docker", "Tailwind CSS"]
            admin_user.profile.location = "İstanbul, TR"
            admin_user.profile.github_url = "https://github.com"
            admin_user.profile.save()

        # 2. Demo Geliştirici 1: Burak (Backend & AI)
        burak, _ = User.objects.get_or_create(
            username='burak_dev',
            defaults={
                'email': 'burak@devconnect.dev',
                'first_name': 'Burak',
                'last_name': 'Yılmaz',
            }
        )
        burak.set_password('password123')
        burak.save()
        burak.profile.bio = "Python ve Django sevdalısı backend mimarı. Dağıtık sistemler ve LLM tabanlı uygulamalar geliştiriyorum."
        burak.profile.specialization = "backend"
        burak.profile.skills = ["Python", "Django", "FastAPI", "PostgreSQL", "Redis", "Celery", "Docker"]
        burak.profile.location = "Ankara, Türkiye"
        burak.profile.github_url = "https://github.com"
        burak.profile.linkedin_url = "https://linkedin.com"
        burak.profile.save()

        # 3. Demo Geliştirici 2: Zeynep (UI/UX & Frontend)
        zeynep, _ = User.objects.get_or_create(
            username='zeynep_ux',
            defaults={
                'email': 'zeynep@devconnect.dev',
                'first_name': 'Zeynep',
                'last_name': 'Kaya',
            }
        )
        zeynep.set_password('password123')
        zeynep.save()
        zeynep.profile.bio = "Kullanıcı deneyimi odaklı dijital ürün tasarımcısı ve modern frontend geliştirici. Figma & Tailwind CSS tutkunu."
        zeynep.profile.specialization = "uiux"
        zeynep.profile.skills = ["Figma", "Tailwind CSS", "React", "Next.js", "Design Systems", "TypeScript"]
        zeynep.profile.location = "İzmir, Türkiye"
        zeynep.profile.github_url = "https://github.com"
        zeynep.profile.linkedin_url = "https://linkedin.com"
        zeynep.profile.website_url = "https://zeynepdesign.dev"
        zeynep.profile.save()

        # 4. Demo Geliştirici 3: Can (Fullstack & Mobile)
        can, _ = User.objects.get_or_create(
            username='can_fullstack',
            defaults={
                'email': 'can@devconnect.dev',
                'first_name': 'Can',
                'last_name': 'Demir',
            }
        )
        can.set_password('password123')
        can.save()
        can.profile.bio = "Mobil ve web dünyasını birleştiren Full Stack geliştirici. Flutter ve bulut mimarileri üzerine çalışıyorum."
        can.profile.specialization = "fullstack"
        can.profile.skills = ["Flutter", "Dart", "Django", "Vue.js", "AWS", "GraphQL"]
        can.profile.location = "Berlin / Uzaktan"
        can.profile.github_url = "https://github.com"
        can.profile.save()

        # 5. Demo Projeler
        p1, _ = Project.objects.get_or_create(
            slug='devpulse-yapay-zeka-kod-analiz-motoru',
            defaults={
                'title': 'DevPulse — Yapay Zeka Destekli Kod İnceleme & Analiz Motoru',
                'author': burak,
                'category': 'ai',
                'description': """### DevPulse Nedir?
DevPulse, Git depolarındaki Pull Request'leri gerçek zamanlı olarak inceleyen ve güvenlik zafiyetlerini, kod kokularını (code smells) tespit eden açık kaynaklı bir inceleme botudur.

### Temel Özellikler
- **AST Tabanlı Analiz**: Python ve TypeScript kodlarını soyut sözdizim ağacı seviyesinde analiz eder.
- **LLM Entegrasyonu**: Bulunan problemleri geliştiriciye açıklayıcı ve çözüm önerisi içeren yorumlar olarak PR altına iletir.
- **Webhook Entegrasyonu**: GitHub ve GitLab webhooklarını dinleyerek otomatik tetiklenir.

```python
# Örnek AST kontrol kancası
def inspect_security_context(node):
    if isinstance(node, ast.Call) and getattr(node.func, 'id', '') == 'eval':
        return SecurityWarning("eval() fonksiyonu doğrudan kod enjeksiyonu riski taşır!")
```
                """,
                'demo_url': 'https://example.com/devpulse-demo',
                'github_url': 'https://github.com/example/devpulse',
                'tags': ['Python', 'FastAPI', 'AST', 'LangChain', 'Docker'],
                'views_count': 142
            }
        )
        p1.likes.set([admin_user, zeynep, can])

        p2, _ = Project.objects.get_or_create(
            slug='aurora-modern-tasarim-sistemi',
            defaults={
                'title': 'Aurora UI — Erişilebilir ve Modüler Tasarım Sistemi',
                'author': zeynep,
                'category': 'uiux',
                'description': """### Aurora UI Hakkında
Modern web uygulamaları için WCAG 2.1 AA erişilebilirlik standartlarına tam uyumlu, 40'tan fazla özelleştirilebilir bileşene sahip bir tasarım kütüphanesi.

### Bileşen Yelpazesi
- Dark / Light mod akıllı kontrast geçişleri
- Klavye navigasyonu ve ekran okuyucu uyumu
- Mikro etkileşimler ve pürüzsüz animasyonlar
- Figma Tokens ile doğrudan kod senkronizasyonu
                """,
                'demo_url': 'https://example.com/aurora-ui',
                'github_url': 'https://github.com/example/aurora-design-system',
                'tags': ['Figma', 'Tailwind CSS', 'React', 'Storybook', 'a11y'],
                'views_count': 238
            }
        )
        p2.likes.set([burak, can])

        p3, _ = Project.objects.get_or_create(
            slug='taskflow-cevrimdisi-calisan-gorev-yonetimi',
            defaults={
                'title': 'TaskFlow — Çevrimdışı (Offline-First) Ekip Görev Yönetimi',
                'author': can,
                'category': 'web',
                'description': """### TaskFlow
İnternet bağlantınız kopsa bile çalışmaya devam eden, CRDT (Conflict-free Replicated Data Types) algoritması ile veri çakışmalarını çözen yeni nesil proje panosu.

### Mimari
- **Frontend**: Vue 3 + Pinia + Tailwind
- **Backend**: Django REST Framework + Channels (WebSockets)
- **Veri Senkronizasyonu**: IndexedDB ve Yjs
                """,
                'demo_url': 'https://example.com/taskflow',
                'github_url': 'https://github.com/example/taskflow',
                'tags': ['Django', 'Vue.js', 'WebSockets', 'Tailwind CSS', 'IndexedDB'],
                'views_count': 189
            }
        )
        p3.likes.set([burak, zeynep, admin_user])

        p4, _ = Project.objects.get_or_create(
            slug='cloudpilot-kubernetes-gozlemleme-paneli',
            defaults={
                'title': 'CloudPilot — Mikroservis ve K8s Sağlık Paneli',
                'author': burak,
                'category': 'devops',
                'description': """### CloudPilot
Kubernetes podlarının CPU, bellek ve ağ metriklerini Prometheus üzerinden toplayan ve görselleştiren hafif bir gözlemleme (observability) arayüzü.
                """,
                'tags': ['Kubernetes', 'Prometheus', 'Go', 'Docker', 'Grafana'],
                'views_count': 95
            }
        )
        p4.likes.set([can])

        # 6. Demo Yorumlar
        Comment.objects.get_or_create(
            project=p1,
            author=zeynep,
            defaults={'content': 'Harika bir proje Burak! Özellikle PR altına yapılan LLM yorumları çok faydalı gözüküyor. Arayüz için Aurora UI bileşenlerini kullanabiliriz.'}
        )
        Comment.objects.get_or_create(
            project=p1,
            author=can,
            defaults={'content': 'Mimari çok temiz. Docker Compose ile yerel ortamda çalıştırmak sadece 1 dakikamı aldı. Eline sağlık!'}
        )
        Comment.objects.get_or_create(
            project=p2,
            author=burak,
            defaults={'content': 'Erişilebilirlik (a11y) detayları muazzam düşünülmüş Zeynep, tebrikler!'}
        )

        # 7. Demo İş İlanları
        JobPosting.objects.get_or_create(
            title='Senior Full-Stack Python & Django Developer',
            company_name='Vortex Cloud Technologies',
            defaults={
                'author': admin_user,
                'location_type': 'remote',
                'location': 'Dünya Çapı / Tam Uzaktan',
                'job_type': 'full_time',
                'salary_range': '$4,500 - $6,500 / Ay',
                'apply_url': 'https://example.com/careers/senior-django',
                'deadline': date.today() + timedelta(days=30),
                'description': """### Rol Hakkında
Vortex Cloud bünyesinde yüksek trafikli SaaS platformumuzun backend ve REST API mimarisini geliştirecek kıdemli Python & Django geliştirici arıyoruz.

### Aranan Nitelikler
- En az 4 yıl Django / Django REST Framework deneyimi
- PostgreSQL performans optimizasyonu ve indeksleme bilgisi
- Redis, Celery ve kuyruk mimarilerinde deneyim
- Modern frontend teknolojilerine (Tailwind, Vue veya React) aşinalık
                """
            }
        )

        JobPosting.objects.get_or_create(
            title='UI/UX Designer & Design System Specialist',
            company_name='Nova Digital Studio',
            defaults={
                'author': zeynep,
                'location_type': 'hybrid',
                'location': 'İstanbul (Levent)',
                'job_type': 'full_time',
                'salary_range': '95.000 TL - 125.000 TL / Ay',
                'apply_url': 'mailto:hr@novastudio.dev',
                'deadline': date.today() + timedelta(days=20),
                'description': """### Rol Tanımı
Yenilikçi fintech ve e-ticaret projelerimiz için uçtan uca kullanıcı deneyimi tasarımı yapacak ve tasarım sistemimizi ölçekleyecek UI/UX uzmanı arıyoruz.
                """
            }
        )

        JobPosting.objects.get_or_create(
            title='DevOps & Cloud Platform Mühendisi',
            company_name='HyperScale Labs',
            defaults={
                'author': burak,
                'location_type': 'remote',
                'location': 'Türkiye Geneli',
                'job_type': 'contract',
                'salary_range': '110.000 TL - 140.000 TL / Ay',
                'apply_url': 'https://example.com/careers/devops',
                'deadline': date.today() + timedelta(days=45),
                'description': """AWS ve Kubernetes altyapılarımızın otomasyonu, CI/CD pipeline'larının iyileştirilmesi ve gözlemlenebilirlik araçlarının kurulumu."""
            }
        )

        self.stdout.write(self.style.SUCCESS("Demo verileri başarıyla oluşturuldu!"))
        self.stdout.write(self.style.SUCCESS("Superuser: admin | Parola: admin123"))
        self.stdout.write(self.style.SUCCESS("Geliştiriciler: burak_dev, zeynep_ux, can_fullstack | Parola: password123"))
