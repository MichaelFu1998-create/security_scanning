def save(self):
        """
        Resend a verification email to the provided address.

        If the provided email is already verified no action is taken.
        """
        try:
            email = models.EmailAddress.objects.get(
                email=self.validated_data["email"], is_verified=False
            )

            logger.debug(
                "Resending verification email to %s",
                self.validated_data["email"],
            )

            email.send_confirmation()
        except models.EmailAddress.DoesNotExist:
            logger.debug(
                "Not resending verification email to %s because the address "
                "doesn't exist in the database.",
                self.validated_data["email"],
            )