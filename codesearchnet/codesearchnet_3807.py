def format_command_subsection(self, ctx, formatter, commands, header):
        """Writes help text for a sub-section of commands,
        specifically to be reused for resource commands
        and system/configuration commands.
        """
        rows = []
        for subcommand in commands:
            cmd = self.get_command(ctx, subcommand)
            # What is this, the tool lied about a command.  Ignore it
            if cmd is None:
                continue

            help = cmd.short_help or ''
            rows.append((subcommand, help))

        if rows:
            with formatter.section(header):
                formatter.write_dl(rows)