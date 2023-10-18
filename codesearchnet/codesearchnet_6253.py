def delete_model_genes(cobra_model, gene_list,
                       cumulative_deletions=True, disable_orphans=False):
    """delete_model_genes will set the upper and lower bounds for reactions
    catalysed by the genes in gene_list if deleting the genes means that
    the reaction cannot proceed according to
    cobra_model.reactions[:].gene_reaction_rule

    cumulative_deletions: False or True.  If True then any previous
    deletions will be maintained in the model.

    """
    if disable_orphans:
        raise NotImplementedError("disable_orphans not implemented")
    if not hasattr(cobra_model, '_trimmed'):
        cobra_model._trimmed = False
        cobra_model._trimmed_genes = []
        cobra_model._trimmed_reactions = {}  # Store the old bounds in here.
    # older models have this
    if cobra_model._trimmed_genes is None:
        cobra_model._trimmed_genes = []
    if cobra_model._trimmed_reactions is None:
        cobra_model._trimmed_reactions = {}
    # Allow a single gene to be fed in as a string instead of a list.
    if not hasattr(gene_list, '__iter__') or \
            hasattr(gene_list, 'id'):  # cobra.Gene has __iter__
        gene_list = [gene_list]

    if not hasattr(gene_list[0], 'id'):
        if gene_list[0] in cobra_model.genes:
                tmp_gene_dict = dict([(x.id, x) for x in cobra_model.genes])
        else:
            # assume we're dealing with names if no match to an id
            tmp_gene_dict = dict([(x.name, x) for x in cobra_model.genes])
        gene_list = [tmp_gene_dict[x] for x in gene_list]

    # Make the genes non-functional
    for x in gene_list:
        x.functional = False

    if cumulative_deletions:
        gene_list.extend(cobra_model._trimmed_genes)
    else:
        undelete_model_genes(cobra_model)

    for the_reaction in find_gene_knockout_reactions(cobra_model, gene_list):
        # Running this on an already deleted reaction will overwrite the
        # stored reaction bounds.
        if the_reaction in cobra_model._trimmed_reactions:
            continue
        old_lower_bound = the_reaction.lower_bound
        old_upper_bound = the_reaction.upper_bound
        cobra_model._trimmed_reactions[the_reaction] = (old_lower_bound,
                                                        old_upper_bound)
        the_reaction.lower_bound = 0.
        the_reaction.upper_bound = 0.
        cobra_model._trimmed = True

    cobra_model._trimmed_genes = list(set(cobra_model._trimmed_genes +
                                          gene_list))