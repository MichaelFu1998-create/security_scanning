def finalize(self, result=None):
        """
        Clean up any created database and schema.
        """
        if not self.settings_path:
            # short circuit if no settings file can be found
            return

        from django.test.utils import teardown_test_environment
        from django.db import connection
        from django.conf import settings

        self.call_plugins_method('beforeDestroyTestDb', settings, connection)
        try:
            connection.creation.destroy_test_db(
                self.old_db,
                verbosity=self.verbosity,
            )
        except Exception:
            # If we can't tear down the test DB, don't worry about it.
            pass
        self.call_plugins_method('afterDestroyTestDb', settings, connection)

        self.call_plugins_method(
            'beforeTeardownTestEnv', settings, teardown_test_environment)
        teardown_test_environment()
        self.call_plugins_method('afterTeardownTestEnv', settings)