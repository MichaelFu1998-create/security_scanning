def update(self, instance, validated_data):
        """
        Update the instance the serializer is bound to.

        Args:
            instance:
                The instance the serializer is bound to.
            validated_data:
                The data to update the serializer with.

        Returns:
            The updated instance.
        """
        is_primary = validated_data.pop("is_primary", False)

        instance = super(EmailSerializer, self).update(
            instance, validated_data
        )

        if is_primary:
            instance.set_primary()

        return instance