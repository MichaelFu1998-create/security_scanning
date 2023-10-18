def _check_required(sbase, value, attribute):
    """Get required attribute from SBase.

    Parameters
    ----------
    sbase : libsbml.SBase
    value : existing value
    attribute: name of attribute

    Returns
    -------
    attribute value (or value if already set)
    """

    if (value is None) or (value == ""):
        msg = "Required attribute '%s' cannot be found or parsed in '%s'" % \
              (attribute, sbase)
        if hasattr(sbase, "getId") and sbase.getId():
            msg += " with id '%s'" % sbase.getId()
        elif hasattr(sbase, "getName") and sbase.getName():
            msg += " with name '%s'" % sbase.getName()
        elif hasattr(sbase, "getMetaId") and sbase.getMetaId():
            msg += " with metaId '%s'" % sbase.getName()
        raise CobraSBMLError(msg)
    return value