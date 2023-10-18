def is_boundary_type(reaction, boundary_type, external_compartment):
    """Check whether a reaction is an exchange reaction.

    Arguments
    ---------
    reaction : cobra.Reaction
        The reaction to check.
    boundary_type : str
        What boundary type to check for. Must be one of
        "exchange", "demand", or "sink".
    external_compartment : str
        The id for the external compartment.

    Returns
    -------
    boolean
        Whether the reaction looks like the requested type. Might be based
        on a heuristic.
    """
    # Check if the reaction has an annotation. Annotations dominate everything.
    sbo_term = reaction.annotation.get("sbo", "")
    if isinstance(sbo_term, list):
        sbo_term = sbo_term[0]
    sbo_term = sbo_term.upper()

    if sbo_term == sbo_terms[boundary_type]:
        return True
    if sbo_term in [sbo_terms[k] for k in sbo_terms if k != boundary_type]:
        return False

    # Check if the reaction is in the correct compartment (exterior or inside)
    correct_compartment = external_compartment in reaction.compartments
    if boundary_type != "exchange":
        correct_compartment = not correct_compartment

    # Check if the reaction has the correct reversibility
    rev_type = True
    if boundary_type == "demand":
        rev_type = not reaction.reversibility
    elif boundary_type == "sink":
        rev_type = reaction.reversibility

    return (reaction.boundary and not
            any(ex in reaction.id for ex in excludes[boundary_type]) and
            correct_compartment and rev_type)