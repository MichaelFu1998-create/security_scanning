def begin(self):
        """
        Create the test database and schema, if needed, and switch the
        connection over to that database. Then call install() to install
        all apps listed in the loaded settings module.
        """
        for plugin in self.nose_config.plugins.plugins:
            if getattr(plugin, 'django_plugin', False):
                self.django_plugins.append(plugin)

        os.environ['DJANGO_SETTINGS_MODULE'] = self.settings_module

        if self.conf.addPaths:
            map(add_path, self.conf.where)

        try:
            __import__(self.settings_module)
            self.settings_path = self.settings_module
        except ImportError:
            # Settings module is not found in PYTHONPATH. Try to do
            # some funky backwards crawling in directory tree, ie. add
            # the working directory (and any package parents) to
            # sys.path before trying to import django modules;
            # otherwise, they won't be able to find project.settings
            # if the working dir is project/ or project/..

            self.settings_path = get_settings_path(self.settings_module)

            if not self.settings_path:
                # short circuit if no settings file can be found
                raise RuntimeError("Can't find Django settings file!")

            add_path(self.settings_path)
            sys.path.append(self.settings_path)

        from django.conf import settings

        # Some Django code paths evaluate differently
        # between DEBUG and not DEBUG.  Example of this include the url
        # dispatcher when 404's are hit.  Django's own test runner forces DEBUG
        # to be off.
        settings.DEBUG = False

        self.call_plugins_method('beforeConnectionSetup', settings)

        from django.core import management
        from django.test.utils import setup_test_environment

        if hasattr(settings, 'DATABASES'):
            self.old_db = settings.DATABASES['default']['NAME']
        else:
            self.old_db = settings.DATABASE_NAME
        from django.db import connections

        self._monkeypatch_test_classes()

        for connection in connections.all():
            self.call_plugins_method(
                'beforeTestSetup', settings, setup_test_environment,
                connection)
        try:
            setup_test_environment()
        except RuntimeError:  # Django 1.11 + multiprocess this happens.
            pass
        import django
        if hasattr(django, 'setup'):
            django.setup()

        self.call_plugins_method('afterTestSetup', settings)

        management.get_commands()
        # Ensure that nothing (eg. South) steals away our syncdb command
        if self.django_version < self.DJANGO_1_7:
            management._commands['syncdb'] = 'django.core'

        for connection in connections.all():
            self.call_plugins_method(
                'beforeTestDb', settings, connection, management)
            connection.creation.create_test_db(
                verbosity=self.verbosity,
                autoclobber=True,
            )
            logger.debug("Running syncdb")
            self._num_syncdb_calls += 1
            self.call_plugins_method('afterTestDb', settings, connection)
        self.store_original_transaction_methods()