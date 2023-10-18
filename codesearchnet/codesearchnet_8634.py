def handle(self, *args, **options):
        """
        Unlink inactive EnterpriseCustomer(s) SAP learners.
        """
        channels = self.get_integrated_channels(options)

        for channel in channels:
            channel_code = channel.channel_code()
            channel_pk = channel.pk
            if channel_code == 'SAP':
                # Transmit the learner data to each integrated channel
                unlink_inactive_learners.delay(channel_code, channel_pk)