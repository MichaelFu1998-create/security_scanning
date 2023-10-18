def sudo(self, password=None):
        """
        Enter sudo mode
        """
        if self.username == 'root':
            raise ValueError('Already root user')
        password = self.validate_password(password)
        stdin, stdout, stderr = self.exec_command('sudo su')
        stdin.write("%s\n" % password)
        stdin.flush()
        errors = stderr.read()
        if errors:
            raise ValueError(errors)