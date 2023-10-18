def create(self, validated_data):
        """
        Create a new email and send a confirmation to it.

        Returns:
            The newly creating ``EmailAddress`` instance.
        """
        email_query = models.EmailAddress.objects.filter(
            email=self.validated_data["email"]
        )

        if email_query.exists():
            email = email_query.get()

            email.send_duplicate_notification()
        else:
            email = super(EmailSerializer, self).create(validated_data)
            email.send_confirmation()

            user = validated_data.get("user")
            query = models.EmailAddress.objects.filter(
                is_primary=True, user=user
            )

            if not query.exists():
                email.set_primary()

        return email