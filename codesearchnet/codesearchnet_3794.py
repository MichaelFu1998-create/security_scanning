def set_or_reset_runtime_param(self, key, value):
        """Maintains the context of the runtime settings for invoking
        a command.

        This should be called by a click.option callback, and only
        called once for each setting for each command invocation.

        If the setting exists, it follows that the runtime settings are
        stale, so the entire runtime settings are reset.
        """
        if self._runtime.has_option('general', key):
            self._runtime = self._new_parser()

        if value is None:
            return
        settings._runtime.set('general', key.replace('tower_', ''),
                              six.text_type(value))