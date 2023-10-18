def validate(self, data):
        """
        Validate the provided data.

        Returns:
            dict:
                The validated data.

        Raises:
            serializers.ValidationError:
                If the provided password is invalid.
        """
        user = self._confirmation.email.user

        if (
            app_settings.EMAIL_VERIFICATION_PASSWORD_REQUIRED
            and not user.check_password(data["password"])
        ):
            raise serializers.ValidationError(
                _("The provided password is invalid.")
            )

        # Add email to returned data
        data["email"] = self._confirmation.email.email

        return data