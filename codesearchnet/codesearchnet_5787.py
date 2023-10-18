def http(self, *args, **kwargs):
        """Returns an authorized http instance.

        Must only be called from within an @oauth_required decorated method, or
        from within an @oauth_aware decorated method where has_credentials()
        returns True.

        Args:
            *args: Positional arguments passed to httplib2.Http constructor.
            **kwargs: Positional arguments passed to httplib2.Http constructor.
        """
        return self.credentials.authorize(
            transport.get_http_object(*args, **kwargs))