def commit(self, *args, **kwargs):
        """Store changes on current instance in database and index it."""
        return super(Deposit, self).commit(*args, **kwargs)