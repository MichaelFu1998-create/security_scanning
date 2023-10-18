def help(self, msg, args):
        """Displays help for each command"""
        output = []
        if len(args) == 0:
            commands = sorted(self._bot.dispatcher.commands.items(), key=itemgetter(0))
            commands = filter(lambda x: x[1].is_subcmd is False, commands)
            # Filter commands if auth is enabled, hide_admin_commands is enabled, and user is not admin
            if self._should_filter_help_commands(msg.user):
                commands = filter(lambda x: x[1].admin_only is False, commands)
            for name, cmd in commands:
                output.append(self._get_short_help_for_command(name))
        else:
            name = '!' + args[0]
            output = [self._get_help_for_command(name)]
        return '\n'.join(output)