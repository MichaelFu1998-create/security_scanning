def clean_channel_worker_username(self):
        """
        Clean enterprise channel worker user form field

        Returns:
            str: the cleaned value of channel user username for transmitting courses metadata.
        """
        channel_worker_username = self.cleaned_data['channel_worker_username'].strip()

        try:
            User.objects.get(username=channel_worker_username)
        except User.DoesNotExist:
            raise ValidationError(
                ValidationMessages.INVALID_CHANNEL_WORKER.format(
                    channel_worker_username=channel_worker_username
                )
            )

        return channel_worker_username