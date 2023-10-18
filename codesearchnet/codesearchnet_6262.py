def find_boundary_types(model, boundary_type, external_compartment=None):
    """Find specific boundary reactions.

    Arguments
    ---------
    model : cobra.Model
        A cobra model.
    boundary_type : str
        What boundary type to check for. Must be one of
        "exchange", "demand", or "sink".
    external_compartment : str or None
        The id for the external compartment. If None it will be detected
        automatically.

    Returns
    -------
    list of cobra.reaction
        A list of likely boundary reactions of a user defined type.
    """
    if not model.boundary:
        LOGGER.warning("There are no boundary reactions in this model. "
                       "Therefore specific types of boundary reactions such "
                       "as 'exchanges', 'demands' or 'sinks' cannot be "
                       "identified.")
        return []
    if external_compartment is None:
        external_compartment = find_external_compartment(model)
    return model.reactions.query(
        lambda r: is_boundary_type(r, boundary_type, external_compartment))