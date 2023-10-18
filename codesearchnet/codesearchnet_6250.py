def prune_unused_reactions(cobra_model):
    """Remove reactions with no assigned metabolites, returns pruned model

    Parameters
    ----------
    cobra_model: class:`~cobra.core.Model.Model` object
        the model to remove unused reactions from

    Returns
    -------
    output_model: class:`~cobra.core.Model.Model` object
        input model with unused reactions removed
    reactions_to_prune: list of class:`~cobra.core.reaction.Reaction`
        list of reactions that were removed
    """

    output_model = cobra_model.copy()
    reactions_to_prune = [r for r in output_model.reactions
                          if len(r.metabolites) == 0]
    output_model.remove_reactions(reactions_to_prune)
    return output_model, reactions_to_prune