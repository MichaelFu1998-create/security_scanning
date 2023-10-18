def load_django_settings(self):
        """
        Loads Django settings for the current site and sets them so Django internals can be run.
        """
        r = self.local_renderer

        # Save environment variables so we can restore them later.
        _env = {}
        save_vars = ['ALLOW_CELERY', 'DJANGO_SETTINGS_MODULE']
        for var_name in save_vars:
            _env[var_name] = os.environ.get(var_name)

        try:

            # Allow us to import local app modules.
            if r.env.local_project_dir:
                sys.path.insert(0, r.env.local_project_dir)

            #TODO:remove this once bug in django-celery has been fixed
            os.environ['ALLOW_CELERY'] = '0'

#             print('settings_module:', r.format(r.env.settings_module))
            os.environ['DJANGO_SETTINGS_MODULE'] = r.format(r.env.settings_module)
#             os.environ['CELERY_LOADER'] = 'django'
#             os.environ['SITE'] = r.genv.SITE or r.genv.default_site
#             os.environ['ROLE'] = r.genv.ROLE or r.genv.default_role

            # In Django >= 1.7, fixes the error AppRegistryNotReady: Apps aren't loaded yet
            # Disabling, in Django >= 1.10, throws exception:
            # RuntimeError: Model class django.contrib.contenttypes.models.ContentType
            # doesn't declare an explicit app_label and isn't in an application in INSTALLED_APPS.
#             try:
#                 from django.core.wsgi import get_wsgi_application
#                 application = get_wsgi_application()
#             except (ImportError, RuntimeError):
#                 raise
#                 print('Unable to get wsgi application.')
#                 traceback.print_exc()

            # In Django >= 1.7, fixes the error AppRegistryNotReady: Apps aren't loaded yet
            try:
                import django
                django.setup()
            except AttributeError:
                # This doesn't exist in Django < 1.7, so ignore it.
                pass

            # Load Django settings.
            settings = self.get_settings()
            try:
                from django.contrib import staticfiles
                from django.conf import settings as _settings

                # get_settings() doesn't raise ImportError but returns None instead
                if settings is not None:
                    for k, v in settings.__dict__.items():
                        setattr(_settings, k, v)
                else:
                    raise ImportError
            except (ImportError, RuntimeError):
                print('Unable to load settings.')
                traceback.print_exc()

        finally:
            # Restore environment variables.
            for var_name, var_value in _env.items():
                if var_value is None:
                    del os.environ[var_name]
                else:
                    os.environ[var_name] = var_value

        return settings