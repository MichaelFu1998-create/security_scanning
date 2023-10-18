def patch_settings(config_data):
    """
    Modify the settings file created by Django injecting the django CMS
    configuration

    :param config_data: configuration data
    """
    import django
    current_django_version = LooseVersion(django.__version__)
    declared_django_version = LooseVersion(config_data.django_version)

    if not os.path.exists(config_data.settings_path):
        sys.stderr.write(
            'Error while creating target project, '
            'please check the given configuration: {0}\n'.format(config_data.settings_path)
        )
        return sys.exit(5)

    if current_django_version.version[:2] != declared_django_version.version[:2]:
        sys.stderr.write(
            'Currently installed Django version {} differs from the declared {}. '
            'Please check the given `--django-version` installer argument, your virtualenv '
            'configuration and any package forcing a different Django version'
            '\n'.format(
                current_django_version, declared_django_version
            )
        )
        return sys.exit(9)

    overridden_settings = (
        'MIDDLEWARE_CLASSES', 'MIDDLEWARE', 'INSTALLED_APPS', 'TEMPLATE_LOADERS',
        'TEMPLATE_CONTEXT_PROCESSORS', 'TEMPLATE_DIRS', 'LANGUAGES'
    )
    extra_settings = ''

    with open(config_data.settings_path, 'r') as fd_original:
        original = fd_original.read()

    # extra settings reading
    if config_data.extra_settings and os.path.exists(config_data.extra_settings):
        with open(config_data.extra_settings, 'r') as fd_extra:
            extra_settings = fd_extra.read()

    original = original.replace('# -*- coding: utf-8 -*-\n', '')

    if config_data.aldryn:  # pragma: no cover
        DATA_DIR = (
            'DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), \'dist\')\n'
        )
        STATICFILES_DIR = 'os.path.join(BASE_DIR, \'static\'),'
    else:
        DATA_DIR = 'DATA_DIR = os.path.dirname(os.path.dirname(__file__))\n'
        STATICFILES_DIR = 'os.path.join(BASE_DIR, \'{0}\', \'static\'),'.format(
            config_data.project_name
        )

    original = data.DEFAULT_PROJECT_HEADER + DATA_DIR + original
    original += 'MEDIA_URL = \'/media/\'\n'
    original += 'MEDIA_ROOT = os.path.join(DATA_DIR, \'media\')\n'
    original += 'STATIC_ROOT = os.path.join(DATA_DIR, \'static\')\n'
    original += """
STATICFILES_DIRS = (
    {0}
)
""".format(STATICFILES_DIR)
    original = original.replace('# -*- coding: utf-8 -*-\n', '')

    # I18N
    if config_data.i18n == 'no':
        original = original.replace('I18N = True', 'I18N = False')
        original = original.replace('L10N = True', 'L10N = False')

    # TZ
    if config_data.use_timezone == 'no':
        original = original.replace('USE_TZ = True', 'USE_TZ = False')

    if config_data.languages:
        original = original.replace(
            'LANGUAGE_CODE = \'en-us\'', 'LANGUAGE_CODE = \'{0}\''.format(config_data.languages[0])
        )
    if config_data.timezone:
        original = original.replace(
            'TIME_ZONE = \'UTC\'', 'TIME_ZONE = \'{0}\''.format(config_data.timezone)
        )

    for item in overridden_settings:
        if declared_django_version >= LooseVersion('1.9'):
            item_re = re.compile(r'{0} = [^\]]+\]'.format(item), re.DOTALL | re.MULTILINE)
        else:
            item_re = re.compile(r'{0} = [^\)]+\)'.format(item), re.DOTALL | re.MULTILINE)
        original = item_re.sub('', original)
    # TEMPLATES is special, so custom regexp needed
    if declared_django_version >= LooseVersion('2.0'):
        item_re = re.compile(r'TEMPLATES = .+\},\n\s+\},\n]$', re.DOTALL | re.MULTILINE)
    else:
        item_re = re.compile(r'TEMPLATES = .+\]$', re.DOTALL | re.MULTILINE)
    original = item_re.sub('', original)
    # DATABASES is a dictionary, so different regexp needed
    item_re = re.compile(r'DATABASES = [^\}]+\}[^\}]+\}', re.DOTALL | re.MULTILINE)
    original = item_re.sub('', original)
    if original.find('SITE_ID') == -1:
        original += 'SITE_ID = 1\n\n'

    original += _build_settings(config_data)
    # Append extra settings at the end of the file
    original += ('\n' + extra_settings)

    with open(config_data.settings_path, 'w') as fd_dest:
        fd_dest.write(original)