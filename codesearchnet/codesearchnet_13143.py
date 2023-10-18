def Async(cls, token, session=None, **options):
        """Returns the client in async mode."""
        return cls(token, session=session, is_async=True, **options)