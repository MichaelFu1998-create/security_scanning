def handle(self, *args, **options):
        """
        Transmit the learner data for the EnterpriseCustomer(s) to the active integration channels.
        """
        # Ensure that we were given an api_user name, and that User exists.
        api_username = options['api_user']
        try:
            User.objects.get(username=api_username)
        except User.DoesNotExist:
            raise CommandError(_('A user with the username {username} was not found.').format(username=api_username))

        # Transmit the learner data to each integrated channel
        for integrated_channel in self.get_integrated_channels(options):
            transmit_learner_data.delay(api_username, integrated_channel.channel_code(), integrated_channel.pk)