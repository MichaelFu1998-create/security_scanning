def exec_command(self, cmd):
        """
        Proceed with caution, if you run a command that causes a prompt and then
        try to read/print the stdout it's going to block forever

        Returns
        -------
        (stdin, stdout, stderr)
        """
        if self.pwd is not None:
            cmd = 'cd %s ; %s' % (self.pwd, cmd)
        if self.interactive:
            print(cmd)
        return self.con.exec_command(cmd)