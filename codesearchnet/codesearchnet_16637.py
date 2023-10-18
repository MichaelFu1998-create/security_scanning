def get_queryset(self):
        """
        Return all unexpired password reset tokens.
        """
        oldest = timezone.now() - app_settings.PASSWORD_RESET_EXPIRATION
        queryset = super(ValidPasswordResetTokenManager, self).get_queryset()

        return queryset.filter(created_at__gt=oldest)