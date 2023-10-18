def save(self):
        """
        Send out a password reset if the provided data is valid.

        If the provided email address exists and is verified, a reset
        email is sent to the address.

        Returns:
            The password reset token if it was returned and ``None``
            otherwise.
        """
        try:
            email = models.EmailAddress.objects.get(
                email=self.validated_data["email"], is_verified=True
            )
        except models.EmailAddress.DoesNotExist:
            return None

        token = models.PasswordResetToken.objects.create(email=email)
        token.send()

        return token