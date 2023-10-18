def shell(self):
        """
        Opens a Django focussed Python shell.
        Essentially the equivalent of running `manage.py shell`.
        """
        r = self.local_renderer
        if '@' in self.genv.host_string:
            r.env.shell_host_string = self.genv.host_string
        else:
            r.env.shell_host_string = '{user}@{host_string}'
        r.env.shell_default_dir = self.genv.shell_default_dir_template
        r.env.shell_interactive_djshell_str = self.genv.interactive_shell_template
        r.run_or_local('ssh -t -i {key_filename} {shell_host_string} "{shell_interactive_djshell_str}"')