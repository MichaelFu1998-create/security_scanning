def authenticate(self, request, email=None, password=None, username=None):
        """
        Attempt to authenticate a set of credentials.

        Args:
            request:
                The request associated with the authentication attempt.
            email:
                The user's email address.
            password:
                The user's password.
            username:
                An alias for the ``email`` field. This is provided for
                compatability with Django's built in authentication
                views.

        Returns:
            The user associated with the provided credentials if they
            are valid. Returns ``None`` otherwise.
        """
        email = email or username

        try:
            email_instance = models.EmailAddress.objects.get(
                is_verified=True, email=email
            )
        except models.EmailAddress.DoesNotExist:
            return None

        user = email_instance.user

        if user.check_password(password):
            return user

        return None