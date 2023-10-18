def unlink_inactive_learners(channel_code, channel_pk):
    """
    Task to unlink inactive learners of provided integrated channel.

    Arguments:
        channel_code (str): Capitalized identifier for the integrated channel
        channel_pk (str): Primary key for identifying integrated channel

    """
    start = time.time()
    integrated_channel = INTEGRATED_CHANNEL_CHOICES[channel_code].objects.get(pk=channel_pk)
    LOGGER.info('Processing learners to unlink inactive users using configuration: [%s]', integrated_channel)

    # Note: learner data transmission code paths don't raise any uncaught exception, so we don't need a broad
    # try-except block here.
    integrated_channel.unlink_inactive_learners()

    duration = time.time() - start
    LOGGER.info(
        'Unlink inactive learners task for integrated channel configuration [%s] took [%s] seconds',
        integrated_channel,
        duration
    )