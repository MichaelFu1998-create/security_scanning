def validate_email(self, email):
        """
        Validate the provided email address.

        The email address is first modified to match the RFC spec.
        Namely, the domain portion of the email is lowercased.

        Returns:
            The validated email address.

        Raises:
            serializers.ValidationError:
                If the serializer is bound and the provided email
                doesn't match the existing address.
        """
        user, domain = email.rsplit("@", 1)
        email = "@".join([user, domain.lower()])

        if self.instance and email and self.instance.email != email:
            raise serializers.ValidationError(
                _(
                    "Existing emails may not be edited. Create a new one "
                    "instead."
                )
            )

        return email