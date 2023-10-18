def remove_genes(cobra_model, gene_list, remove_reactions=True):
    """remove genes entirely from the model

    This will also simplify all gene_reaction_rules with this
    gene inactivated."""
    gene_set = {cobra_model.genes.get_by_id(str(i)) for i in gene_list}
    gene_id_set = {i.id for i in gene_set}
    remover = _GeneRemover(gene_id_set)
    ast_rules = get_compiled_gene_reaction_rules(cobra_model)
    target_reactions = []
    for reaction, rule in iteritems(ast_rules):
        if reaction.gene_reaction_rule is None or \
                len(reaction.gene_reaction_rule) == 0:
            continue
        # reactions to remove
        if remove_reactions and not eval_gpr(rule, gene_id_set):
            target_reactions.append(reaction)
        else:
            # if the reaction is not removed, remove the gene
            # from its gpr
            remover.visit(rule)
            new_rule = ast2str(rule)
            if new_rule != reaction.gene_reaction_rule:
                reaction.gene_reaction_rule = new_rule
    for gene in gene_set:
        cobra_model.genes.remove(gene)
        # remove reference to the gene in all groups
        associated_groups = cobra_model.get_associated_groups(gene)
        for group in associated_groups:
            group.remove_members(gene)
    cobra_model.remove_reactions(target_reactions)