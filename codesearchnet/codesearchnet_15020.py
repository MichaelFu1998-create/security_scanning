def description(_dummy_ctx, markdown=False):
    """Dump project metadata for Jenkins Description Setter Plugin."""
    cfg = config.load()
    markup = 'md' if markdown else 'html'
    description_file = cfg.rootjoin("build/project.{}".format(markup))
    notify.banner("Creating {} file for Jenkins...".format(description_file))

    long_description = cfg.project.long_description
    long_description = long_description.replace('\n\n', '</p>\n<p>')
    long_description = re.sub(r'(\W)``([^`]+)``(\W)', r'\1<tt>\2</tt>\3', long_description)

    text = DESCRIPTION_TEMPLATES[markup].format(
        keywords=', '.join(cfg.project.keywords),
        classifiers='\n'.join(cfg.project.classifiers),
        classifiers_indented='    ' + '\n    '.join(cfg.project.classifiers),
        packages=', '.join(cfg.project.packages),
        long_description_html='<p>{}</p>'.format(long_description),
        ##data='\n'.join(["%s=%r" % i for i in cfg.project.iteritems()]),
        **cfg)
    with io.open(description_file, 'w', encoding='utf-8') as handle:
        handle.write(text)