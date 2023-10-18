def validate_key(self, key):
        """
        Validate the provided reset key.

        Returns:
            The validated key.

        Raises:
            serializers.ValidationError:
                If the provided key does not exist.
        """
        if not models.PasswordResetToken.valid_tokens.filter(key=key).exists():
            raise serializers.ValidationError(
                _("The provided reset token does not exist, or is expired.")
            )

        return key