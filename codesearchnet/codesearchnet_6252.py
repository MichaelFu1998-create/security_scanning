def find_gene_knockout_reactions(cobra_model, gene_list,
                                 compiled_gene_reaction_rules=None):
    """identify reactions which will be disabled when the genes are knocked out

    cobra_model: :class:`~cobra.core.Model.Model`

    gene_list: iterable of :class:`~cobra.core.Gene.Gene`

    compiled_gene_reaction_rules: dict of {reaction_id: compiled_string}
        If provided, this gives pre-compiled gene_reaction_rule strings.
        The compiled rule strings can be evaluated much faster. If a rule
        is not provided, the regular expression evaluation will be used.
        Because not all gene_reaction_rule strings can be evaluated, this
        dict must exclude any rules which can not be used with eval.

    """
    potential_reactions = set()
    for gene in gene_list:
        if isinstance(gene, string_types):
            gene = cobra_model.genes.get_by_id(gene)
        potential_reactions.update(gene._reaction)
    gene_set = {str(i) for i in gene_list}
    if compiled_gene_reaction_rules is None:
        compiled_gene_reaction_rules = {r: parse_gpr(r.gene_reaction_rule)[0]
                                        for r in potential_reactions}

    return [r for r in potential_reactions
            if not eval_gpr(compiled_gene_reaction_rules[r], gene_set)]