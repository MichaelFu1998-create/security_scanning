def do_EOF(self, line):
        """
        Exit shell and shoebot

        Alias for exit.
        """
        print(self.response_prompt, file=self.stdout)
        return self.do_exit(line)