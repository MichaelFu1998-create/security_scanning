def shell(self, name='default', user=None, password=None, root=0, verbose=1, write_password=1, no_db=0, no_pw=0):
        """
        Opens a SQL shell to the given database, assuming the configured database
        and user supports this feature.
        """
        raise NotImplementedError