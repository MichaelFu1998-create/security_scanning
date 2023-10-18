def list_misc_commands(self):
        """Returns a list of global commands, realted to CLI
        configuration or system management in general.
        """
        answer = set([])
        for cmd_name in misc.__all__:
            answer.add(cmd_name)
        return sorted(answer)