from datetime import datetime


def platform_context(request):
    """
    Global context processor available in all templates.
    """
    return {
        'PLATFORM_NAME': 'DevConnect',
        'PLATFORM_TAGLINE': 'Yazılımcılar ve Tasarımcılar İçin Vitrin & İlan Platformu',
        'CURRENT_YEAR': datetime.now().year,
    }
