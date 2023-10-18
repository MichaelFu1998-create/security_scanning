def do_help(self, arg):
        """
        Show help on all commands.
        """
        print(self.response_prompt, file=self.stdout)
        return cmd.Cmd.do_help(self, arg)