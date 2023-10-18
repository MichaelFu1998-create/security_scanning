def shell(self, expect=pexpect):
        """
        Connects the database client shell to the database.

        Parameters
        ----------
        expect_module: str
            the database to which backup will be restored.
        """
        dsn = self.connection_dsn()
        log.debug('connection string: %s' % dsn)
        child = expect.spawn('psql "%s"' % dsn)
        if self._connect_args['password'] is not None:
            child.expect('Password: ')
            child.sendline(self._connect_args['password'])
        child.interact()