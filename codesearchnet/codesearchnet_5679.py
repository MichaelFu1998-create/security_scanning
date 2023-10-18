def parse_command_line(self, argv=None):
        """
        Overriden to check for conflicting flags
        Since notebook version doesn't do it well (or, indeed, at all)
        """
        conflicting_flags = set(['--user', '--system', '--sys-prefix'])

        if len(conflicting_flags.intersection(set(argv))) > 1:
            raise serverextensions.ArgumentConflict(
                'cannot specify more than one of user, sys_prefix, or system')
        return super(ToggleJupyterTensorboardApp,
                     self).parse_command_line(argv)