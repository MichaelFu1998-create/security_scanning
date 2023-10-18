def create(self, validated_data):
        """
        Create a new user from the data passed to the serializer.

        If the provided email has not been verified yet, the user is
        created and a verification email is sent to the address.
        Otherwise we send a notification to the email address that
        someone attempted to register with an email that's already been
        verified.

        Args:
            validated_data (dict):
                The data passed to the serializer after it has been
                validated.

        Returns:
            A new user created from the provided data.
        """
        email = validated_data.pop("email")
        password = validated_data.pop("password")

        # We don't save the user instance yet in case the provided email
        # address already exists.
        user = get_user_model()(**validated_data)
        user.set_password(password)

        # We set an ephemeral email property so that it is included in
        # the data returned by the serializer.
        user.email = email

        email_query = models.EmailAddress.objects.filter(email=email)

        if email_query.exists():
            existing_email = email_query.get()
            existing_email.send_duplicate_notification()
        else:
            user.save()

            email_instance = models.EmailAddress.objects.create(
                email=email, user=user
            )
            email_instance.send_confirmation()

            signals.user_registered.send(sender=self.__class__, user=user)

        return user