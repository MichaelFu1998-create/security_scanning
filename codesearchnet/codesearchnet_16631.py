def save(self):
        """
        Reset the user's password if the provided information is valid.
        """
        token = models.PasswordResetToken.objects.get(
            key=self.validated_data["key"]
        )

        token.email.user.set_password(self.validated_data["password"])
        token.email.user.save()

        logger.info("Reset password for %s", token.email.user)

        token.delete()