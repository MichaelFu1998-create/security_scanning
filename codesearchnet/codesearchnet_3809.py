def list_commands(self, ctx):
        """Return a list of commands present in the commands and resources
        folders, but not subcommands.
        """
        commands = set(self.list_resource_commands())
        commands.union(set(self.list_misc_commands()))
        return sorted(commands)