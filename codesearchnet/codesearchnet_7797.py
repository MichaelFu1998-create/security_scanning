def copy_files(config_data):
    """
    It's a little rude actually: it just overwrites the django-generated urls.py
    with a custom version and put other files in the project directory.

    :param config_data: configuration data
    """
    if config_data.i18n == 'yes':
        urlconf_path = os.path.join(os.path.dirname(__file__), '../config/urls_i18n.py')
    else:
        urlconf_path = os.path.join(os.path.dirname(__file__), '../config/urls_noi18n.py')
    share_path = os.path.join(os.path.dirname(__file__), '../share')
    template_path = os.path.join(share_path, 'templates')
    if config_data.aldryn:  # pragma: no cover
        media_project, static_main, static_project, template_target = _install_aldryn(config_data)
    else:
        media_project = os.path.join(config_data.project_directory, 'media')
        static_main = os.path.join(config_data.project_path, 'static')
        static_project = os.path.join(config_data.project_directory, 'static')
        template_target = os.path.join(config_data.project_path, 'templates')
        if config_data.templates and os.path.isdir(config_data.templates):
            template_path = config_data.templates
        elif config_data.bootstrap:
            template_path = os.path.join(template_path, 'bootstrap')
        else:
            template_path = os.path.join(template_path, 'basic')

    shutil.copy(urlconf_path, config_data.urlconf_path)
    if media_project:
        os.makedirs(media_project)
    if static_main:
        os.makedirs(static_main)
    if not os.path.exists(static_project):
        os.makedirs(static_project)
    if not os.path.exists(template_target):
        os.makedirs(template_target)
    for filename in glob.glob(os.path.join(template_path, '*.html')):
        if os.path.isfile(filename):
            shutil.copy(filename, template_target)

    if config_data.noinput and not config_data.no_user:
        script_path = os.path.join(share_path, 'create_user.py')
        if os.path.isfile(script_path):
            shutil.copy(script_path, os.path.join(config_data.project_path, '..'))

    if config_data.starting_page:
        for filename in glob.glob(os.path.join(share_path, 'starting_page.*')):
            if os.path.isfile(filename):
                shutil.copy(filename, os.path.join(config_data.project_path, '..'))