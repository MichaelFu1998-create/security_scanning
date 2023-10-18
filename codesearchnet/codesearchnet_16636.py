def create(self, *args, **kwargs):
        """
        Create a new email address.
        """
        is_primary = kwargs.pop("is_primary", False)

        with transaction.atomic():
            email = super(EmailAddressManager, self).create(*args, **kwargs)

            if is_primary:
                email.set_primary()

        return email