def undelete_model_genes(cobra_model):
    """Undoes the effects of a call to delete_model_genes in place.

    cobra_model:  A cobra.Model which will be modified in place

    """

    if cobra_model._trimmed_genes is not None:
        for x in cobra_model._trimmed_genes:
            x.functional = True

    if cobra_model._trimmed_reactions is not None:
        for the_reaction, (lower_bound, upper_bound) in \
                cobra_model._trimmed_reactions.items():
            the_reaction.lower_bound = lower_bound
            the_reaction.upper_bound = upper_bound

    cobra_model._trimmed_genes = []
    cobra_model._trimmed_reactions = {}
    cobra_model._trimmed = False