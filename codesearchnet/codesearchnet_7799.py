def _build_settings(config_data):
    """
    Build the django CMS settings dictionary

    :param config_data: configuration data
    """
    spacer = '    '
    text = []
    vars = get_settings()

    vars.MIDDLEWARE_CLASSES.insert(0, vars.APPHOOK_RELOAD_MIDDLEWARE_CLASS)

    processors = vars.TEMPLATE_CONTEXT_PROCESSORS + vars.TEMPLATE_CONTEXT_PROCESSORS_3
    text.append(data.TEMPLATES_1_8.format(
        loaders=(',\n' + spacer * 4).join([
            "'{0}'".format(var) for var in vars.TEMPLATE_LOADERS
            if (
                LooseVersion(config_data.django_version) < LooseVersion('2.0') or
                'eggs' not in var
            )
        ]),
        processors=(',\n' + spacer * 4).join(["'{0}'".format(var) for var in processors]),
        dirs="os.path.join(BASE_DIR, '{0}', 'templates'),".format(config_data.project_name)
    ))

    if LooseVersion(config_data.django_version) >= LooseVersion('1.10'):
        text.append('MIDDLEWARE = [\n{0}{1}\n]'.format(
            spacer, (',\n' + spacer).join(['\'{0}\''.format(var)
                                           for var in vars.MIDDLEWARE_CLASSES])
        ))
    else:
        text.append('MIDDLEWARE_CLASSES = [\n{0}{1}\n]'.format(
            spacer, (',\n' + spacer).join(["'{0}'".format(var)
                                           for var in vars.MIDDLEWARE_CLASSES])
        ))

    apps = list(vars.INSTALLED_APPS)
    apps = list(vars.CMS_3_HEAD) + apps
    apps.extend(vars.TREEBEARD_APPS)
    apps.extend(vars.CMS_3_APPLICATIONS)

    if not config_data.no_plugins:
        apps.extend(vars.FILER_PLUGINS_3)

    if config_data.aldryn:  # pragma: no cover
        apps.extend(vars.ALDRYN_APPLICATIONS)
    if config_data.reversion and LooseVersion(config_data.cms_version) < LooseVersion('3.4'):
        apps.extend(vars.REVERSION_APPLICATIONS)
    text.append('INSTALLED_APPS = [\n{0}{1}\n]'.format(
        spacer, (',\n' + spacer).join(['\'{0}\''.format(var) for var in apps] +
                                      ['\'{0}\''.format(config_data.project_name)])
    ))

    text.append('LANGUAGES = (\n{0}{1}\n{0}{2}\n)'.format(
        spacer, '## Customize this',
        ('\n' + spacer).join(['(\'{0}\', gettext(\'{0}\')),'.format(item) for item in config_data.languages])  # NOQA
    ))

    cms_langs = deepcopy(vars.CMS_LANGUAGES)
    for lang in config_data.languages:
        lang_dict = {'code': lang, 'name': lang}
        lang_dict.update(copy(cms_langs['default']))
        cms_langs[1].append(lang_dict)
    cms_text = ['CMS_LANGUAGES = {']
    cms_text.append('{0}{1}'.format(spacer, '## Customize this'))
    for key, value in iteritems(cms_langs):
        if key == 'default':
            cms_text.append('{0}\'{1}\': {{'.format(spacer, key))
            for config_name, config_value in iteritems(value):
                cms_text.append('{0}\'{1}\': {2},'.format(spacer * 2, config_name, config_value))
            cms_text.append('{0}}},'.format(spacer))
        else:
            cms_text.append('{0}{1}: ['.format(spacer, key))
            for lang in value:
                cms_text.append('{0}{{'.format(spacer * 2))
                for config_name, config_value in iteritems(lang):
                    if config_name == 'code':
                        cms_text.append('{0}\'{1}\': \'{2}\','.format(spacer * 3, config_name, config_value))  # NOQA
                    elif config_name == 'name':
                        cms_text.append('{0}\'{1}\': gettext(\'{2}\'),'.format(spacer * 3, config_name, config_value))  # NOQA
                    else:
                        cms_text.append('{0}\'{1}\': {2},'.format(
                            spacer * 3, config_name, config_value
                        ))
                cms_text.append('{0}}},'.format(spacer * 2))
            cms_text.append('{0}],'.format(spacer))
    cms_text.append('}')

    text.append('\n'.join(cms_text))

    if config_data.bootstrap:
        cms_templates = 'CMS_TEMPLATES_BOOTSTRAP'
    else:
        cms_templates = 'CMS_TEMPLATES'

    text.append('CMS_TEMPLATES = (\n{0}{1}\n{0}{2}\n)'.format(
        spacer, '## Customize this',
        (',\n' + spacer).join(
            ['(\'{0}\', \'{1}\')'.format(*item) for item in getattr(vars, cms_templates)]
        )
    ))

    text.append('CMS_PERMISSION = {0}'.format(vars.CMS_PERMISSION))
    text.append('CMS_PLACEHOLDER_CONF = {0}'.format(vars.CMS_PLACEHOLDER_CONF))

    database = ['\'{0}\': {1}'.format(key, format_val(val)) for key, val in sorted(config_data.db_parsed.items(), key=lambda x: x[0])]  # NOQA
    text.append(textwrap.dedent("""
        DATABASES = {{
            'default': {{
                {0}
            }}
        }}""").strip().format((',\n' + spacer * 2).join(database)))  # NOQA

    DJANGO_MIGRATION_MODULES = _detect_migration_layout(vars, apps)

    text.append('MIGRATION_MODULES = {{\n{0}{1}\n}}'.format(
        spacer, (',\n' + spacer).join(
            ['\'{0}\': \'{1}\''.format(*item) for item in DJANGO_MIGRATION_MODULES.items()]
        )
    ))

    if config_data.filer:
        text.append('THUMBNAIL_PROCESSORS = (\n{0}{1}\n)'.format(
            spacer, (',\n' + spacer).join(
                ['\'{0}\''.format(var) for var in vars.THUMBNAIL_PROCESSORS]
            )
        ))
    return '\n\n'.join(text)