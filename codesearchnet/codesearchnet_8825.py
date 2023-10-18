def get_idp_choices():
    """
    Get a list of identity providers choices for enterprise customer.

    Return:
        A list of choices of all identity providers, None if it can not get any available identity provider.
    """
    try:
        from third_party_auth.provider import Registry   # pylint: disable=redefined-outer-name
    except ImportError as exception:
        LOGGER.warning("Could not import Registry from third_party_auth.provider")
        LOGGER.warning(exception)
        Registry = None  # pylint: disable=redefined-outer-name

    first = [("", "-" * 7)]
    if Registry:
        return first + [(idp.provider_id, idp.name) for idp in Registry.enabled()]
    return None