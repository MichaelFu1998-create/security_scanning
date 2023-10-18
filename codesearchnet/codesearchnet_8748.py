def handle(self, *args, **options):
        """
        Transmit the courseware data for the EnterpriseCustomer(s) to the active integration channels.
        """
        username = options['catalog_user']

        # Before we do a whole bunch of database queries, make sure that the user we were passed exists.
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            raise CommandError('A user with the username {} was not found.'.format(username))

        channels = self.get_integrated_channels(options)

        for channel in channels:
            channel_code = channel.channel_code()
            channel_pk = channel.pk
            transmit_content_metadata.delay(username, channel_code, channel_pk)