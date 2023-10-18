def vagrant_settings(self, name='', *args, **kwargs):
        """
        Context manager that sets a vagrant VM
        as the remote host.

        Use this context manager inside a task to run commands
        on your current Vagrant box::

            from burlap.vagrant import vagrant_settings

            with vagrant_settings():
                run('hostname')
        """
        config = self.ssh_config(name)

        extra_args = self._settings_dict(config)
        kwargs.update(extra_args)

        return self.settings(*args, **kwargs)