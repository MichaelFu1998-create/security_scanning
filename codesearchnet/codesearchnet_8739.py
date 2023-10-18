def transmit_content_metadata(username, channel_code, channel_pk):
    """
    Task to send content metadata to each linked integrated channel.

    Arguments:
        username (str): The username of the User to be used for making API requests to retrieve content metadata.
        channel_code (str): Capitalized identifier for the integrated channel.
        channel_pk (str): Primary key for identifying integrated channel.

    """
    start = time.time()
    api_user = User.objects.get(username=username)
    integrated_channel = INTEGRATED_CHANNEL_CHOICES[channel_code].objects.get(pk=channel_pk)
    LOGGER.info('Transmitting content metadata to integrated channel using configuration: [%s]', integrated_channel)
    try:
        integrated_channel.transmit_content_metadata(api_user)
    except Exception:  # pylint: disable=broad-except
        LOGGER.exception(
            'Transmission of content metadata failed for user [%s] and for integrated '
            'channel with code [%s] and id [%s].', username, channel_code, channel_pk
        )
    duration = time.time() - start
    LOGGER.info(
        'Content metadata transmission task for integrated channel configuration [%s] took [%s] seconds',
        integrated_channel,
        duration
    )