from django.templatetags.static import static


def site_brand(request):
    """Global site branding context processor.

    Provides SITE_NAME, SITE_LOGO, and SITE_TAGLINE to every template.
    Change the values here once and they propagate to every page —
    sidebar, topbar, landing page, PDF letterhead, error pages, etc.
    """
    return {
        'SITE_NAME': 'PTI Clinic',
        'SITE_LOGO': static('images/pti-logo.jpg'),
        'SITE_TAGLINE': 'Petroleum Training Institute Telemedicine Portal',
    }
