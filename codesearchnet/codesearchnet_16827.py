def process_minter(value):
    """Load minter from PIDStore registry based on given value.

    :param value: Name of the minter.
    :returns: The minter.
    """
    try:
        return current_pidstore.minters[value]
    except KeyError:
        raise click.BadParameter(
            'Unknown minter {0}. Please use one of {1}.'.format(
                value, ', '.join(current_pidstore.minters.keys())
            )
        )