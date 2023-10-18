def apply_defaults(self, commands):
        """ apply default settings to commands
            not static, shadow "self" in eval
        """
        for command in commands:
            if 'action' in command and "()" in command['action']:
                command['action'] = eval("self.{}".format(command['action']))
            if command['keys'][0].startswith('-'):
                if 'required' not in command:
                    command['required'] = False