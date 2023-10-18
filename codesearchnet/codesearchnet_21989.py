def start(info):
    """Run the dev server.

    Uses `django_extensions <http://pypi.python.org/pypi/django-extensions/0.5>`, if
    available, to provide `runserver_plus`.

    Set the command to use with `options.paved.django.runserver`
    Set the port to use with `options.paved.django.runserver_port`
    """
    cmd = options.paved.django.runserver

    if cmd == 'runserver_plus':
        try:
            import django_extensions
        except ImportError:
            info("Could not import django_extensions. Using default runserver.")
            cmd = 'runserver'

    port = options.paved.django.runserver_port
    if port:
        cmd = '%s %s' % (cmd, port)

    call_manage(cmd)