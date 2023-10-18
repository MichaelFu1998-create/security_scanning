def payload_class_for_element_name(element_name):
    """Return a payload class for given element name."""
    logger.debug(" looking up payload class for element: {0!r}".format(
                                                                element_name))
    logger.debug("  known: {0!r}".format(STANZA_PAYLOAD_CLASSES))
    if element_name in STANZA_PAYLOAD_CLASSES:
        return STANZA_PAYLOAD_CLASSES[element_name]
    else:
        return XMLPayload