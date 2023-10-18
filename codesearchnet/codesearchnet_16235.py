def autodiscover():
    """
    Imports all available previews classes.
    """
    from django.conf import settings
    for application in settings.INSTALLED_APPS:
        module = import_module(application)

        if module_has_submodule(module, 'emails'):
            emails = import_module('%s.emails' % application)
            try:
                import_module('%s.emails.previews' % application)
            except ImportError:
                # Only raise the exception if this module contains previews and
                # there was a problem importing them. (An emails module that
                # does not contain previews is not an error.)
                if module_has_submodule(emails, 'previews'):
                    raise