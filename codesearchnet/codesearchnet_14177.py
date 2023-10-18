def pangocairo_create_context(cr):
    """
    If python-gi-cairo is not installed, using PangoCairo.create_context
    dies with an unhelpful KeyError, check for that and output somethig
    useful.
    """
    # TODO move this to core.backend
    try:
        return PangoCairo.create_context(cr)
    except KeyError as e:
        if e.args == ('could not find foreign type Context',):
            raise ShoebotInstallError("Error creating PangoCairo missing dependency: python-gi-cairo")
        else:
            raise