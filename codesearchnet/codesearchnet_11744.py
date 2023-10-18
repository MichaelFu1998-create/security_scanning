def shell(self, gui=0, command='', dryrun=None, shell_interactive_cmd_str=None):
        """
        Opens an SSH connection.
        """
        from burlap.common import get_hosts_for_site

        if dryrun is not None:
            self.dryrun = dryrun

        r = self.local_renderer

        if r.genv.SITE != r.genv.default_site:
            shell_hosts = get_hosts_for_site()
            if shell_hosts:
                r.genv.host_string = shell_hosts[0]

        r.env.SITE = r.genv.SITE or r.genv.default_site

        if int(gui):
            r.env.shell_default_options.append('-X')

        if 'host_string' not in self.genv or not self.genv.host_string:
            if 'available_sites' in self.genv and r.env.SITE not in r.genv.available_sites:
                raise Exception('No host_string set. Unknown site %s.' % r.env.SITE)
            else:
                raise Exception('No host_string set.')

        if '@' in r.genv.host_string:
            r.env.shell_host_string = r.genv.host_string
        else:
            r.env.shell_host_string = '{user}@{host_string}'

        if command:
            r.env.shell_interactive_cmd_str = command
        else:
            r.env.shell_interactive_cmd_str = r.format(shell_interactive_cmd_str or r.env.shell_interactive_cmd)

        r.env.shell_default_options_str = ' '.join(r.env.shell_default_options)
        if self.is_local:
            self.vprint('Using direct local.')
            cmd = '{shell_interactive_cmd_str}'
        elif r.genv.key_filename:
            self.vprint('Using key filename.')
            # If host_string contains the port, then strip it off and pass separately.
            port = r.env.shell_host_string.split(':')[-1]
            if port.isdigit():
                r.env.shell_host_string = r.env.shell_host_string.split(':')[0] + (' -p %s' % port)
            cmd = 'ssh -t {shell_default_options_str} -i {key_filename} {shell_host_string} "{shell_interactive_cmd_str}"'
        elif r.genv.password:
            self.vprint('Using password.')
            cmd = 'ssh -t {shell_default_options_str} {shell_host_string} "{shell_interactive_cmd_str}"'
        else:
            # No explicit password or key file needed?
            self.vprint('Using nothing.')
            cmd = 'ssh -t {shell_default_options_str} {shell_host_string} "{shell_interactive_cmd_str}"'
        r.local(cmd)