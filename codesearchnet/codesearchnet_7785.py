def parse(args):
    """
    Define the available arguments
    """
    from tzlocal import get_localzone

    try:
        timezone = get_localzone()
        if isinstance(timezone, pytz.BaseTzInfo):
            timezone = timezone.zone
    except Exception:  # pragma: no cover
        timezone = 'UTC'
    if timezone == 'local':
        timezone = 'UTC'
    parser = argparse.ArgumentParser(description="""Bootstrap a django CMS project.
Major usage modes:

- wizard: djangocms -w -p /path/whatever project_name: ask for all the options through a
          CLI wizard.

- batch: djangocms project_name: runs with the default values plus any
         additional option provided (see below) with no question asked.

- config file: djangocms_installer --config-file /path/to/config.ini project_name: reads values
               from an ini-style config file.

Check https://djangocms-installer.readthedocs.io/en/latest/usage.html for detailed usage
information.
""", formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--config-file', dest='config_file', action='store',
                        default=None,
                        help='Configuration file for djangocms_installer')
    parser.add_argument('--config-dump', dest='config_dump', action='store',
                        default=None,
                        help='Dump configuration file with current args')
    parser.add_argument('--db', '-d', dest='db', action=DbAction,
                        default='sqlite://localhost/project.db',
                        help='Database configuration (in URL format). '
                             'Example: sqlite://localhost/project.db')
    parser.add_argument('--i18n', '-i', dest='i18n', action='store',
                        choices=('yes', 'no'),
                        default='yes', help='Activate Django I18N / L10N setting; this is '
                                            'automatically activated if more than '
                                            'language is provided')
    parser.add_argument('--use-tz', '-z', dest='use_timezone', action='store',
                        choices=('yes', 'no'),
                        default='yes', help='Activate Django timezone support')
    parser.add_argument('--timezone', '-t', dest='timezone',
                        required=False, default=timezone,
                        action='store', help='Optional default time zone. Example: Europe/Rome')
    parser.add_argument('--reversion', '-e', dest='reversion', action='store',
                        choices=('yes', 'no'),
                        default='yes', help='Install and configure reversion support '
                                            '(only for django CMS 3.2 and 3.3)')
    parser.add_argument('--permissions', dest='permissions', action='store',
                        choices=('yes', 'no'),
                        default='no', help='Activate CMS permission management')
    parser.add_argument('--pip-options', help='pass custom pip options', default='')
    parser.add_argument('--languages', '-l', dest='languages', action='append',
                        help='Languages to enable. Option can be provided multiple times, or as a '
                             'comma separated list. Only language codes supported by Django can '
                             'be used here. Example: en, fr-FR, it-IT')
    parser.add_argument('--django-version', dest='django_version', action='store',
                        choices=data.DJANGO_SUPPORTED,
                        default=data.DJANGO_DEFAULT, help='Django version')
    parser.add_argument('--cms-version', '-v', dest='cms_version', action='store',
                        choices=data.DJANGOCMS_SUPPORTED,
                        default=data.DJANGOCMS_DEFAULT, help='django CMS version')
    parser.add_argument('--parent-dir', '-p', dest='project_directory',
                        default='',
                        action='store', help='Optional project parent directory')
    parser.add_argument('--bootstrap', dest='bootstrap', action='store',
                        choices=('yes', 'no'),
                        default='no', help='Use Twitter Bootstrap Theme')
    parser.add_argument('--templates', dest='templates', action='store',
                        default='no', help='Use custom template set')
    parser.add_argument('--starting-page', dest='starting_page', action='store',
                        choices=('yes', 'no'),
                        default='no', help='Load a starting page with examples after installation '
                                           '(english language only). Choose "no" if you use a '
                                           'custom template set.')
    parser.add_argument(dest='project_name', action='store',
                        help='Name of the project to be created')

    # Command that lists the supported plugins in verbose description
    parser.add_argument('--list-plugins', '-P', dest='plugins', action='store_true',
                        help='List plugins that\'s going to be installed and configured')

    # Command that lists the supported plugins in verbose description
    parser.add_argument('--dump-requirements', '-R', dest='dump_reqs', action='store_true',
                        help='It dumps the requirements that would be installed according to '
                             'parameters given. Together with --requirements argument is useful '
                             'for customizing the virtualenv')

    # Advanced options. These have a predefined default and are not asked
    # by config wizard.
    parser.add_argument('--no-input', '-q', dest='noinput', action='store_true',
                        default=True, help='Don\'t run the configuration wizard, just use the '
                                           'provided values')
    parser.add_argument('--wizard', '-w', dest='wizard', action='store_true',
                        default=False, help='Run the configuration wizard')
    parser.add_argument('--verbose', dest='verbose', action='store_true',
                        default=False,
                        help='Be more verbose and don\'t swallow subcommands output')
    parser.add_argument('--filer', '-f', dest='filer', action='store_true',
                        default=True, help='Install and configure django-filer plugins '
                                           '- Always enabled')
    parser.add_argument('--requirements', '-r', dest='requirements_file', action='store',
                        default=None, help='Externally defined requirements file')
    parser.add_argument('--no-deps', '-n', dest='no_deps', action='store_true',
                        default=False, help='Don\'t install package dependencies')
    parser.add_argument('--no-plugins', dest='no_plugins', action='store_true',
                        default=False, help='Don\'t install plugins')
    parser.add_argument('--no-db-driver', dest='no_db_driver', action='store_true',
                        default=False, help='Don\'t install database package')
    parser.add_argument('--no-sync', '-m', dest='no_sync', action='store_true',
                        default=False, help='Don\'t run syncdb / migrate after bootstrapping')
    parser.add_argument('--no-user', '-u', dest='no_user', action='store_true',
                        default=False, help='Don\'t create the admin user')
    parser.add_argument('--template', dest='template', action='store',
                        default=None, help='The path or URL to load the django project '
                                           'template from.')
    parser.add_argument('--extra-settings', dest='extra_settings', action='store',
                        default=None, help='The path to an file that contains extra settings.')
    parser.add_argument('--skip-empty-check', '-s', dest='skip_project_dir_check',
                        action='store_true',
                        default=False, help='Skip the check if project dir is empty.')
    parser.add_argument('--delete-project-dir', '-c', dest='delete_project_dir',
                        action='store_true',
                        default=False, help='Delete project directory on creation failure.')
    parser.add_argument('--utc', dest='utc',
                        action='store_true',
                        default=False, help='Use UTC timezone.')

    if '--utc' in args:
        for action in parser._positionals._actions:
            if action.dest == 'timezone':
                action.default = 'UTC'

    # If config_args then pretend that config args came from the stdin and run parser again.
    config_args = ini.parse_config_file(parser, args)
    args = parser.parse_args(config_args + args)
    if not args.wizard:
        args.noinput = True
    else:
        args.noinput = False

    if not args.project_directory:
        args.project_directory = args.project_name
    args.project_directory = os.path.abspath(args.project_directory)

    # First of all, check if the project name is valid
    if not validate_project(args.project_name):
        sys.stderr.write(
            'Project name "{0}" is not a valid app name, or it\'s already defined. '
            'Please use only numbers, letters and underscores.\n'.format(args.project_name)
        )
        sys.exit(3)

    # Checking the given path
    setattr(args, 'project_path', os.path.join(args.project_directory, args.project_name).strip())
    if not args.skip_project_dir_check:
        if (os.path.exists(args.project_directory) and
                [path for path in os.listdir(args.project_directory) if not path.startswith('.')]):
            sys.stderr.write(
                'Path "{0}" already exists and is not empty, please choose a different one\n'
                'If you want to use this path anyway use the -s flag to skip this check.\n'
                ''.format(args.project_directory)
            )
            sys.exit(4)

    if os.path.exists(args.project_path):
        sys.stderr.write(
            'Path "{0}" already exists, please choose a different one\n'.format(args.project_path)
        )
        sys.exit(4)

    if args.config_dump and os.path.isfile(args.config_dump):
        sys.stdout.write(
            'Cannot dump because given configuration file "{0}" exists.\n'.format(args.config_dump)
        )
        sys.exit(8)

    args = _manage_args(parser,  args)

    # what do we want here?!
    # * if languages are given as multiple arguments, let's use it as is
    # * if no languages are given, use a default and stop handling it further
    # * if languages are given as a comma-separated list, split it and use the
    #   resulting list.

    if not args.languages:
        try:
            args.languages = [locale.getdefaultlocale()[0].split('_')[0]]
        except Exception:  # pragma: no cover
            args.languages = ['en']
    elif isinstance(args.languages, six.string_types):
        args.languages = args.languages.split(',')
    elif len(args.languages) == 1 and isinstance(args.languages[0], six.string_types):
        args.languages = args.languages[0].split(',')

    args.languages = [lang.strip().lower() for lang in args.languages]
    if len(args.languages) > 1:
        args.i18n = 'yes'
    args.aldryn = False
    args.filer = True

    # Convert version to numeric format for easier checking
    try:
        django_version, cms_version = supported_versions(args.django_version, args.cms_version)
        cms_package = data.PACKAGE_MATRIX.get(
            cms_version, data.PACKAGE_MATRIX[data.DJANGOCMS_LTS]
        )
    except RuntimeError as e:  # pragma: no cover
        sys.stderr.write(compat.unicode(e))
        sys.exit(6)
    if django_version is None:  # pragma: no cover
        sys.stderr.write(
            'Please provide a Django supported version: {0}. Only Major.Minor '
            'version selector is accepted\n'.format(', '.join(data.DJANGO_SUPPORTED))
        )
        sys.exit(6)
    if cms_version is None:  # pragma: no cover
        sys.stderr.write(
            'Please provide a django CMS supported version: {0}. Only Major.Minor '
            'version selector is accepted\n'.format(', '.join(data.DJANGOCMS_SUPPORTED))
        )
        sys.exit(6)

    default_settings = '{}.settings'.format(args.project_name)
    env_settings = os.environ.get('DJANGO_SETTINGS_MODULE', default_settings)
    if env_settings != default_settings:
        sys.stderr.write(
            '`DJANGO_SETTINGS_MODULE` is currently set to \'{0}\' which is not compatible with '
            'djangocms installer.\nPlease unset `DJANGO_SETTINGS_MODULE` and re-run the installer '
            '\n'.format(env_settings)
        )
        sys.exit(10)

    if not getattr(args, 'requirements_file'):
        requirements = []

        # django CMS version check
        if args.cms_version == 'develop':
            requirements.append(cms_package)
            warnings.warn(data.VERSION_WARNING.format('develop', 'django CMS'))
        elif args.cms_version == 'rc':  # pragma: no cover
            requirements.append(cms_package)
        elif args.cms_version == 'beta':  # pragma: no cover
            requirements.append(cms_package)
            warnings.warn(data.VERSION_WARNING.format('beta', 'django CMS'))
        else:
            requirements.append(cms_package)

        if args.cms_version in ('rc', 'develop'):
            requirements.extend(data.REQUIREMENTS['cms-master'])
        elif LooseVersion(cms_version) >= LooseVersion('3.6'):
            requirements.extend(data.REQUIREMENTS['cms-3.6'])
        elif LooseVersion(cms_version) >= LooseVersion('3.5'):
            requirements.extend(data.REQUIREMENTS['cms-3.5'])
        elif LooseVersion(cms_version) >= LooseVersion('3.4'):
            requirements.extend(data.REQUIREMENTS['cms-3.4'])

        if not args.no_db_driver:
            requirements.append(args.db_driver)
        if not args.no_plugins:
            if args.cms_version in ('rc', 'develop'):
                requirements.extend(data.REQUIREMENTS['plugins-master'])
            elif LooseVersion(cms_version) >= LooseVersion('3.6'):
                requirements.extend(data.REQUIREMENTS['plugins-3.6'])
            elif LooseVersion(cms_version) >= LooseVersion('3.5'):
                requirements.extend(data.REQUIREMENTS['plugins-3.5'])
            elif LooseVersion(cms_version) >= LooseVersion('3.4'):
                requirements.extend(data.REQUIREMENTS['plugins-3.4'])
            requirements.extend(data.REQUIREMENTS['filer'])

        if args.aldryn:  # pragma: no cover
            requirements.extend(data.REQUIREMENTS['aldryn'])

        # Django version check
        if args.django_version == 'develop':  # pragma: no cover
            requirements.append(data.DJANGO_DEVELOP)
            warnings.warn(data.VERSION_WARNING.format('develop', 'Django'))
        elif args.django_version == 'beta':  # pragma: no cover
            requirements.append(data.DJANGO_BETA)
            warnings.warn(data.VERSION_WARNING.format('beta', 'Django'))
        else:
            requirements.append('Django<{0}'.format(less_than_version(django_version)))

        if django_version == '1.8':
            requirements.extend(data.REQUIREMENTS['django-1.8'])
        elif django_version == '1.9':
            requirements.extend(data.REQUIREMENTS['django-1.9'])
        elif django_version == '1.10':
            requirements.extend(data.REQUIREMENTS['django-1.10'])
        elif django_version == '1.11':
            requirements.extend(data.REQUIREMENTS['django-1.11'])
        elif django_version == '2.0':
            requirements.extend(data.REQUIREMENTS['django-2.0'])
        elif django_version == '2.1':
            requirements.extend(data.REQUIREMENTS['django-2.1'])

        requirements.extend(data.REQUIREMENTS['default'])

        setattr(args, 'requirements', '\n'.join(requirements).strip())

    # Convenient shortcuts
    setattr(args, 'cms_version', cms_version)
    setattr(args, 'django_version', django_version)
    setattr(args, 'settings_path',
            os.path.join(args.project_directory, args.project_name, 'settings.py').strip())
    setattr(args, 'urlconf_path',
            os.path.join(args.project_directory, args.project_name, 'urls.py').strip())

    if args.config_dump:
        ini.dump_config_file(args.config_dump, args, parser)

    return args