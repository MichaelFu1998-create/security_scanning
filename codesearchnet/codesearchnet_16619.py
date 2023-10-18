def set_primary(self):
        """
        Set this email address as the user's primary email.
        """
        query = EmailAddress.objects.filter(is_primary=True, user=self.user)
        query = query.exclude(pk=self.pk)

        # The transaction is atomic so there is never a gap where a user
        # has no primary email address.
        with transaction.atomic():
            query.update(is_primary=False)

            self.is_primary = True
            self.save()

        logger.info(
            "Set %s as the primary email address for %s.",
            self.email,
            self.user,
        )