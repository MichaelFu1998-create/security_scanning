def get_command(self, ctx, name):
        """Given a command identified by its name, import the appropriate
        module and return the decorated command.

        Resources are automatically commands, but if both a resource and
        a command are defined, the command takes precedence.
        """
        # First, attempt to get a basic command from `tower_cli.api.misc`.
        if name in misc.__all__:
            return getattr(misc, name)

        # No command was found; try to get a resource.
        try:
            resource = tower_cli.get_resource(name)
            return ResSubcommand(resource)
        except ImportError:
            pass

        # Okay, we weren't able to find a command.
        secho('No such command: %s.' % name, fg='red', bold=True)
        sys.exit(2)