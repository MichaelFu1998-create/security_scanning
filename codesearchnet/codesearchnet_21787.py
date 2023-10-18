def command(self):
        '''Command used to launch this application module'''

        cmd = self.config.get('command', None)
        if cmd is None:
            return

        cmd = cmd[platform]
        return cmd['path'], cmd['args']