def validate_key(self, key):
        """
        Validate the provided confirmation key.

        Returns:
            str:
                The validated confirmation key.

        Raises:
            serializers.ValidationError:
                If there is no email confirmation with the given key or
                the confirmation has expired.
        """
        try:
            confirmation = models.EmailConfirmation.objects.select_related(
                "email__user"
            ).get(key=key)
        except models.EmailConfirmation.DoesNotExist:
            raise serializers.ValidationError(
                _("The provided verification key is invalid.")
            )

        if confirmation.is_expired:
            raise serializers.ValidationError(
                _("That verification code has expired.")
            )

        # Cache confirmation instance
        self._confirmation = confirmation

        return key