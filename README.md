# DevConnect — Yazılımcı & Tasarımcı Vitrin Platformu

DevConnect, yazılımcı ve tasarımcıların geliştirdikleri projeleri ve açık kaynak çalışmalarını sergileyebildikleri, toplulukla etkileşime geçebildikleri (beğeni, yorum) ve teknoloji odaklı iş ilanlarına erişebildikleri modern bir web platformudur.

---

## 🛠️ Mimari ve Teknoloji Yığını

- **Backend:** Python 3.11+, Django 5.x / 6.x
- **Veritabanı:** SQLite3 (Geliştirme) / PostgreSQL uyumlu ORM modelleri
- **Frontend:** HTML5, Tailwind CSS (Modern Dark Mode Estetiği), Vanilla JavaScript
- **Kimlik Doğrulama:** `AbstractUser` tabanlı Custom User Modeli ve One-to-One `UserProfile`
- **Tasarım:** Responsive, Developer-first slate/indigo dark tema, cam (glassmorphism) efektleri
- **İçerik:** Markdown formatlı zengin proje ve iş tanımları desteği (`markdown` kütüphanesi)
- **Etkileşim:** Sayfa yenilemesiz AJAX Beğeni (Like) mekanizması

---

## 📂 Dizin Ağacı (Project Directory Tree)

```text
devconnect/
├── manage.py
├── requirements.txt
├── README.md
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── apps/
│   ├── __init__.py
│   ├── core/
│   │   ├── management/commands/seed_data.py
│   │   ├── context_processors.py
│   │   ├── apps.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── accounts/
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── forms.py
│   │   ├── urls.py
│   │   ├── views.py
│   │   ├── admin.py
│   │   └── signals.py
│   ├── projects/
│   │   ├── templatetags/markdown_extras.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── forms.py
│   │   ├── urls.py
│   │   ├── views.py
│   │   └── admin.py
│   └── jobs/
│       ├── apps.py
│       ├── models.py
│       ├── forms.py
│       ├── urls.py
│       ├── views.py
│       └── admin.py
├── static/
│   ├── css/
│   │   └── custom.css
│   └── js/
│       └── main.js
├── media/
│   ├── avatars/
│   └── projects/
└── templates/
    ├── base.html
    ├── components/
    │   ├── navbar.html
    │   ├── footer.html
    │   ├── messages.html
    │   └── project_card.html
    ├── core/
    │   └── home.html
    ├── accounts/
    │   ├── login.html
    │   ├── register.html
    │   ├── profile.html
    │   └── edit_profile.html
    ├── projects/
    │   ├── list.html
    │   ├── detail.html
    │   ├── form.html
    │   └── confirm_delete.html
    └── jobs/
        ├── list.html
        ├── detail.html
        ├── form.html
        └── confirm_delete.html
```

---

## 🚀 Kurulum ve Çalıştırma Adımları

### 1. Sanal Ortam Oluşturma ve Aktifleştirme
```bash
# Proje dizinine gidin
cd devconnect

# Sanal ortamı oluşturun
python -m venv venv

# Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# veya Windows (CMD):
.\venv\Scripts\activate.bat
# Linux/macOS:
source venv/bin/activate
```

### 2. Bağımlılıkların Kurulumu
```bash
pip install -r requirements.txt
```

### 3. Veritabanı Migrasyonları
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Demo Verilerini Yükleme (Önerilen)
Platformu hazır kullanıcılar, projeler, yorumlar ve iş ilanlarıyla test etmek için özel seed komutu:
```bash
python manage.py seed_data
```
> **Hazır Giriş Bilgileri:**
> - **Yönetici (Admin):** Kullanıcı adı: `admin` | Parola: `admin123`
> - **Geliştirici:** Kullanıcı adı: `burak_dev` | Parola: `password123`
> - **Tasarımcı:** Kullanıcı adı: `zeynep_ux` | Parola: `password123`

*(İsteğe bağlı olarak kendi admininizi `python manage.py createsuperuser` ile de oluşturabilirsiniz)*

### 5. Geliştirme Sunucusunu Başlatma
```bash
python manage.py runserver
```

Tarayıcınızdan `http://127.0.0.1:8000/` adresini açarak platformu kullanmaya başlayabilirsiniz!
