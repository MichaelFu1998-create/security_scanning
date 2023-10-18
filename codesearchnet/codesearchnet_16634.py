def validate_email(self, email):
        """
        Validate the provided email address.

        Args:
            email:
                The email address to validate.

        Returns:
            The provided email address, transformed to match the RFC
            spec. Namely, the domain portion of the email must be
            lowercase.
        """
        user, domain = email.rsplit("@", 1)

        return "@".join([user, domain.lower()])