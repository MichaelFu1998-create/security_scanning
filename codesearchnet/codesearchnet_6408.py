def get_domain(context, prefix):
    """
    Return the domain used for the tracking code.  Each service may be
    configured with its own domain (called `<name>_domain`), or a
    django-analytical-wide domain may be set (using `analytical_domain`.

    If no explicit domain is found in either the context or the
    settings, try to get the domain from the contrib sites framework.
    """
    domain = context.get('%s_domain' % prefix)
    if domain is None:
        domain = context.get('analytical_domain')
    if domain is None:
        domain = getattr(settings, '%s_DOMAIN' % prefix.upper(), None)
    if domain is None:
        domain = getattr(settings, 'ANALYTICAL_DOMAIN', None)
    if domain is None:
        if 'django.contrib.sites' in settings.INSTALLED_APPS:
            from django.contrib.sites.models import Site
            try:
                domain = Site.objects.get_current().domain
            except (ImproperlyConfigured, Site.DoesNotExist):
                pass
    return domain