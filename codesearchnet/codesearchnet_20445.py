def require_authentication(self, request):
        """Ensure we are authenticated."""
        request.user = user = None

        if request.method == 'OPTIONS':
            # Authentication should not be checked on an OPTIONS request.
            return

        for auth in self.meta.authentication:
            user = auth.authenticate(request)
            if user is False:
                # Authentication protocol failed to authenticate;
                # pass the baton.
                continue

            if user is None and not auth.allow_anonymous:
                # Authentication protocol determined the user is
                # unauthenticated.
                auth.unauthenticated()

            # Authentication protocol determined the user is indeed
            # authenticated (or not); Store the user for later reference.
            request.user = user
            return

        if not user and not auth.allow_anonymous:
            # No authenticated user found and protocol doesn't allow
            # anonymous users.
            auth.unauthenticated()