def wait(self, cmd, raise_on_error=True):
        """
        Execute command and wait for it to finish. Proceed with caution because
        if you run a command that causes a prompt this will hang
        """
        _, stdout, stderr = self.exec_command(cmd)
        stdout.channel.recv_exit_status()
        output = stdout.read()
        if self.interactive:
            print(output)
        errors = stderr.read()
        if self.interactive:
            print(errors)
        if errors and raise_on_error:
            raise ValueError(errors)
        return output