def get_identity_provider(provider_id):
    """
    Get Identity Provider with given id.

    Return:
        Instance of ProviderConfig or None.
    """
    try:
        from third_party_auth.provider import Registry   # pylint: disable=redefined-outer-name
    except ImportError as exception:
        LOGGER.warning("Could not import Registry from third_party_auth.provider")
        LOGGER.warning(exception)
        Registry = None  # pylint: disable=redefined-outer-name

    try:
        return Registry and Registry.get(provider_id)
    except ValueError:
        return None