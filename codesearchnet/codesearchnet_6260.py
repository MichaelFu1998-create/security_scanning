def find_external_compartment(model):
    """Find the external compartment in the model.

    Uses a simple heuristic where the external compartment should be the one
    with the most exchange reactions.

    Arguments
    ---------
    model : cobra.Model
        A cobra model.

    Returns
    -------
    str
        The putative external compartment.
    """
    if model.boundary:
        counts = pd.Series(tuple(r.compartments)[0] for r in model.boundary)
        most = counts.value_counts()
        most = most.index[most == most.max()].to_series()
    else:
        most = None
    like_external = compartment_shortlist["e"] + ["e"]
    matches = pd.Series([co in like_external for co in model.compartments],
                        index=model.compartments)

    if matches.sum() == 1:
        compartment = matches.index[matches][0]
        LOGGER.info("Compartment `%s` sounds like an external compartment. "
                    "Using this one without counting boundary reactions" %
                    compartment)
        return compartment
    elif most is not None and matches.sum() > 1 and matches[most].sum() == 1:
        compartment = most[matches[most]][0]
        LOGGER.warning("There are several compartments that look like an "
                       "external compartment but `%s` has the most boundary "
                       "reactions, so using that as the external "
                       "compartment." % compartment)
        return compartment
    elif matches.sum() > 1:
        raise RuntimeError("There are several compartments (%s) that look "
                           "like external compartments but we can't tell "
                           "which one to use. Consider renaming your "
                           "compartments please.")

    if most is not None:
        return most[0]
        LOGGER.warning("Could not identify an external compartment by name and"
                       " choosing one with the most boundary reactions. That "
                       "might be complete nonsense or change suddenly. "
                       "Consider renaming your compartments using "
                       "`Model.compartments` to fix this.")
    # No info in the model, so give up
    raise RuntimeError("The heuristic for discovering an external compartment "
                       "relies on names and boundary reactions. Yet, there "
                       "are neither compartments with recognized names nor "
                       "boundary reactions in the model.")