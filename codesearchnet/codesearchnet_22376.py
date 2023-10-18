def execute(self, command, timeout=None):
        """Execute a shell command."""
        try:
            self.channel = self.ssh.get_transport().open_session()
        except paramiko.SSHException as e:
            self.unknown("Create channel error: %s" % e)
        try:
            self.channel.settimeout(self.args.timeout if not timeout else timeout)
        except socket.timeout as e:
            self.unknown("Settimeout for channel error: %s" % e)
        try:
            self.logger.debug("command: {}".format(command))
            self.channel.exec_command(command)
        except paramiko.SSHException as e:
            self.unknown("Execute command error: %s" % e)
        try:
            self.stdin = self.channel.makefile('wb', -1)
            self.stderr = map(string.strip, self.channel.makefile_stderr('rb', -1).readlines())
            self.stdout = map(string.strip, self.channel.makefile('rb', -1).readlines())
        except Exception as e:
            self.unknown("Get result error: %s" % e)
        try:
            self.status = self.channel.recv_exit_status()
        except paramiko.SSHException as e:
            self.unknown("Get return code error: %s" % e)
        else:
            if self.status != 0:
                self.unknown("Return code: %d , stderr: %s" % (self.status, self.errors))
            else:
                return self.stdout
        finally:
            self.logger.debug("Execute command finish.")