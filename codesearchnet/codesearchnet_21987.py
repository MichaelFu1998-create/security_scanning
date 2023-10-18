def call_manage(cmd, capture=False, ignore_error=False):
    """Utility function to run commands against Django's `django-admin.py`/`manage.py`.

    `options.paved.django.project`: the path to the django project
        files (where `settings.py` typically resides).
        Will fall back to a DJANGO_SETTINGS_MODULE environment variable.

    `options.paved.django.manage_py`: the path where the django
        project's `manage.py` resides.
     """
    settings = (options.paved.django.settings or
                os.environ.get('DJANGO_SETTINGS_MODULE'))
    if settings is None:
        raise BuildFailure("No settings path defined. Use: options.paved.django.settings = 'path.to.project.settings'")
    manage_py = options.paved.django.manage_py
    if manage_py is None:
        manage_py = 'django-admin.py'
    else:
        manage_py = path(manage_py)
        manage_py = 'cd {manage_py.parent}; python ./{manage_py.name}'.format(**locals())
    return util.shv('{manage_py} {cmd} --settings={settings}'.format(**locals()), capture=capture, ignore_error=ignore_error)