def shuffle_channels(image, random_state, channels=None):
    """
    Randomize the order of (color) channels in an image.

    dtype support::

        * ``uint8``: yes; fully tested
        * ``uint16``: yes; indirectly tested (1)
        * ``uint32``: yes; indirectly tested (1)
        * ``uint64``: yes; indirectly tested (1)
        * ``int8``: yes; indirectly tested (1)
        * ``int16``: yes; indirectly tested (1)
        * ``int32``: yes; indirectly tested (1)
        * ``int64``: yes; indirectly tested (1)
        * ``float16``: yes; indirectly tested (1)
        * ``float32``: yes; indirectly tested (1)
        * ``float64``: yes; indirectly tested (1)
        * ``float128``: yes; indirectly tested (1)
        * ``bool``: yes; indirectly tested (1)

        - (1) Indirectly tested via ``ChannelShuffle``.

    Parameters
    ----------
    image : (H,W,[C]) ndarray
        Image of any dtype for which to shuffle the channels.

    random_state : numpy.random.RandomState
        The random state to use for this shuffling operation.

    channels : None or imgaug.ALL or list of int, optional
        Which channels are allowed to be shuffled with each other.
        If this is ``None`` or ``imgaug.ALL``, then all channels may be shuffled. If it is a list of integers,
        then only the channels with indices in that list may be shuffled. (Values start at 0. All channel indices in
        the list must exist in each image.)

    Returns
    -------
    ndarray
        The input image with shuffled channels.

    """
    if image.ndim < 3 or image.shape[2] == 1:
        return image
    nb_channels = image.shape[2]
    all_channels = np.arange(nb_channels)
    is_all_channels = (
        channels is None
        or channels == ia.ALL
        or len(set(all_channels).difference(set(channels))) == 0
    )
    if is_all_channels:
        # note that if this is the case, then 'channels' may be None or imgaug.ALL, so don't simply move the
        # assignment outside of the if/else
        channels_perm = random_state.permutation(all_channels)
        return image[..., channels_perm]
    else:
        channels_perm = random_state.permutation(channels)
        channels_perm_full = all_channels
        for channel_source, channel_target in zip(channels, channels_perm):
            channels_perm_full[channel_source] = channel_target
        return image[..., channels_perm_full]