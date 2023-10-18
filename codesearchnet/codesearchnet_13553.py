def filter_mechanism_list(mechanisms, properties, allow_insecure = False,
                            server_side = False):
    """Filter a mechanisms list only to include those mechanisms that cans
    succeed with the provided properties and are secure enough.

    :Parameters:
        - `mechanisms`: list of the mechanisms names
        - `properties`: available authentication properties
        - `allow_insecure`: allow insecure mechanisms
    :Types:
        - `mechanisms`: sequence of `unicode`
        - `properties`: mapping
        - `allow_insecure`: `bool`

    :returntype: `list` of `unicode`
    """
    # pylint: disable=W0212
    result = []
    for mechanism in mechanisms:
        try:
            if server_side:
                klass = SERVER_MECHANISMS_D[mechanism]
            else:
                klass = CLIENT_MECHANISMS_D[mechanism]
        except KeyError:
            logger.debug(" skipping {0} - not supported".format(mechanism))
            continue
        secure = properties.get("security-layer")
        if not allow_insecure and not klass._pyxmpp_sasl_secure and not secure:
            logger.debug(" skipping {0}, as it is not secure".format(mechanism))
            continue
        if not klass.are_properties_sufficient(properties):
            logger.debug(" skipping {0}, as the properties are not sufficient"
                                                            .format(mechanism))
            continue
        result.append(mechanism)
    return result