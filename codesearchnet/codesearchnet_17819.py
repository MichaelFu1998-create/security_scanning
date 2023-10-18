def _should_use_transaction_isolation(self, test, settings):
        """
        Determine if the given test supports transaction management for
        database rollback test isolation and also whether or not the test has
        opted out of that support.

        Transactions make database rollback much quicker when supported, with
        the caveat that any tests that are explicitly testing transactions
        won't work properly and any tests that depend on external access to the
        test database won't be able to view data created/altered during the
        test.
        """
        if not getattr(test.context, 'use_transaction_isolation', True):
            # The test explicitly says not to use transaction isolation
            return False
        if getattr(settings, 'DISABLE_TRANSACTION_MANAGEMENT', False):
            # Do not use transactions if user has forbidden usage.
            return False
        if hasattr(settings, 'DATABASE_SUPPORTS_TRANSACTIONS'):
            if not settings.DATABASE_SUPPORTS_TRANSACTIONS:
                # The DB doesn't support transactions. Don't try it
                return False

        return True