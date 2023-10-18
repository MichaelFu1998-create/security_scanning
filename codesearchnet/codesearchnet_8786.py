def get_channel_classes(channel_code):
        """
        Assemble a list of integrated channel classes to transmit to.

        If a valid channel type was provided, use it.

        Otherwise, use all the available channel types.
        """
        if channel_code:
            # Channel code is case-insensitive
            channel_code = channel_code.upper()

            if channel_code not in INTEGRATED_CHANNEL_CHOICES:
                raise CommandError(_('Invalid integrated channel: {channel}').format(channel=channel_code))

            channel_classes = [INTEGRATED_CHANNEL_CHOICES[channel_code]]
        else:
            channel_classes = INTEGRATED_CHANNEL_CHOICES.values()

        return channel_classes