def ImpulseNoise(p=0, name=None, deterministic=False, random_state=None):
    """
    Creates an augmenter to apply impulse noise to an image.

    This is identical to ``SaltAndPepper``, except that per_channel is always set to True.

    dtype support::

        See ``imgaug.augmenters.arithmetic.SaltAndPepper``.

    """
    return SaltAndPepper(p=p, per_channel=True, name=name, deterministic=deterministic, random_state=random_state)