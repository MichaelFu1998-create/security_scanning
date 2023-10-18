def validate_is_primary(self, is_primary):
        """
        Validate the provided 'is_primary' parameter.

        Returns:
            The validated 'is_primary' value.

        Raises:
            serializers.ValidationError:
                If the user attempted to mark an unverified email as
                their primary email address.
        """
        # TODO: Setting 'is_primary' to 'False' should probably not be
        #       allowed.
        if is_primary and not (self.instance and self.instance.is_verified):
            raise serializers.ValidationError(
                _(
                    "Unverified email addresses may not be used as the "
                    "primary address."
                )
            )

        return is_primary