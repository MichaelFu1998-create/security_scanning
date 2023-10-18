def prune_unused_metabolites(cobra_model):
    """Remove metabolites that are not involved in any reactions and
    returns pruned model

    Parameters
    ----------
    cobra_model: class:`~cobra.core.Model.Model` object
        the model to remove unused metabolites from

    Returns
    -------
    output_model: class:`~cobra.core.Model.Model` object
        input model with unused metabolites removed
    inactive_metabolites: list of class:`~cobra.core.reaction.Reaction`
        list of metabolites that were removed
    """

    output_model = cobra_model.copy()
    inactive_metabolites = [m for m in output_model.metabolites
                            if len(m.reactions) == 0]
    output_model.remove_metabolites(inactive_metabolites)
    return output_model, inactive_metabolites