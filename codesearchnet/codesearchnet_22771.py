def create_commands(self, commands, parser):
        """ add commands to parser """
        self.apply_defaults(commands)
        def create_single_command(command):
            keys = command['keys']
            del command['keys']
            kwargs = {}
            for item in command:
                kwargs[item] = command[item]
            parser.add_argument(*keys, **kwargs)

        if len(commands) > 1:
            for command in commands:
                create_single_command(command)
        else:
            create_single_command(commands[0])