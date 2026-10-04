/**
 * DevConnect Client-side Utilities
 * - Responsive Mobile Navbar
 * - AJAX Like Toggle
 * - Flash Message Auto-dismiss
 */

document.addEventListener('DOMContentLoaded', () => {
    // 1. Mobile Menu Toggle
    const mobileMenuBtn = document.getElementById('mobile-menu-button');
    const mobileMenu = document.getElementById('mobile-menu');

    if (mobileMenuBtn && mobileMenu) {
        mobileMenuBtn.addEventListener('click', () => {
            mobileMenu.classList.toggle('hidden');
        });
    }

    // 2. Flash Messages Dismissal
    const alertDismissBtns = document.querySelectorAll('[data-dismiss="alert"]');
    alertDismissBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const alertBox = btn.closest('.flash-alert');
            if (alertBox) {
                alertBox.style.opacity = '0';
                setTimeout(() => alertBox.remove(), 300);
            }
        });
    });

    // Auto dismiss after 6 seconds
    setTimeout(() => {
        const alerts = document.querySelectorAll('.flash-alert');
        alerts.forEach(alert => {
            alert.style.transition = 'opacity 0.5s ease-out';
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 500);
        });
    }, 6000);

    // 3. Helper to get CSRF Cookie
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // 4. AJAX Like System
    const likeForms = document.querySelectorAll('.like-form');
    likeForms.forEach(form => {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();

            const actionUrl = form.getAttribute('action');
            const csrfInput = form.querySelector('[name=csrfmiddlewaretoken]');
            const csrfToken = csrfInput ? csrfInput.value : getCookie('csrftoken');
            const likeBtn = form.querySelector('.like-btn');
            const heartIcon = form.querySelector('.heart-icon');
            const likeCounter = form.querySelector('.like-counter');

            try {
                const response = await fetch(actionUrl, {
                    method: 'POST',
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest',
                        'X-CSRFToken': csrfToken,
                        'Accept': 'application/json',
                    }
                });

                if (response.redirected) {
                    window.location.href = response.url;
                    return;
                }

                if (response.ok) {
                    const data = await response.json();
                    
                    if (likeCounter) {
                        likeCounter.textContent = data.total_likes;
                    }

                    if (data.liked) {
                        heartIcon.classList.remove('text-slate-400');
                        heartIcon.classList.add('text-rose-500', 'fill-current');
                        likeBtn.classList.add('bg-rose-500/10', 'border-rose-500/30');
                    } else {
                        heartIcon.classList.remove('text-rose-500', 'fill-current');
                        heartIcon.classList.add('text-slate-400');
                        likeBtn.classList.remove('bg-rose-500/10', 'border-rose-500/30');
                    }
                } else if (response.status === 403 || response.status === 401) {
                    // Redirect to login if unauthenticated
                    window.location.href = '/accounts/login/?next=' + encodeURIComponent(window.location.pathname);
                }
            } catch (err) {
                // Fallback to normal form submit if fetch fails
                form.submit();
            }
        });
    });
});
