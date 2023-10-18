def format_commands(self, ctx, formatter):
        """Extra format methods for multi methods that adds all the commands
        after the options.
        """
        self.format_command_subsection(
            ctx, formatter, self.list_misc_commands(), 'Commands'
        )
        self.format_command_subsection(
            ctx, formatter, self.list_resource_commands(), 'Resources'
        )