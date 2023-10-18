def options(self, parser, env=None):
        """
        Sphinx config file that can optionally take the following python
        template string arguments:

        ``database_name``
        ``database_password``
        ``database_username``
        ``database_host``
        ``database_port``
        ``sphinx_search_data_dir``
        ``searchd_log_dir``
        """
        if env is None:
            env = os.environ
        parser.add_option(
            '--sphinx-config-tpl',
            help='Path to the Sphinx configuration file template.',
        )

        super(SphinxSearchPlugin, self).options(parser, env)