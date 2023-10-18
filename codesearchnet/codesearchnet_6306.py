def rename_genes(cobra_model, rename_dict):
    """renames genes in a model from the rename_dict"""
    recompute_reactions = set()  # need to recomptue related genes
    remove_genes = []
    for old_name, new_name in iteritems(rename_dict):
        # undefined if there a value matches a different key
        # because dict is unordered
        try:
            gene_index = cobra_model.genes.index(old_name)
        except ValueError:
            gene_index = None
        old_gene_present = gene_index is not None
        new_gene_present = new_name in cobra_model.genes
        if old_gene_present and new_gene_present:
            old_gene = cobra_model.genes.get_by_id(old_name)
            # Added in case not renaming some genes:
            if old_gene is not cobra_model.genes.get_by_id(new_name):
                remove_genes.append(old_gene)
                recompute_reactions.update(old_gene._reaction)
        elif old_gene_present and not new_gene_present:
            # rename old gene to new gene
            gene = cobra_model.genes[gene_index]
            # trick DictList into updating index
            cobra_model.genes._dict.pop(gene.id)  # ugh
            gene.id = new_name
            cobra_model.genes[gene_index] = gene
        elif not old_gene_present and new_gene_present:
            pass
        else:  # if not old gene_present and not new_gene_present
            # the new gene's _model will be set by repair
            # This would add genes from rename_dict
            # that are not associated with a rxn
            # cobra_model.genes.append(Gene(new_name))
            pass
    cobra_model.repair()

    class Renamer(NodeTransformer):
        def visit_Name(self, node):
            node.id = rename_dict.get(node.id, node.id)
            return node

    gene_renamer = Renamer()
    for rxn, rule in iteritems(get_compiled_gene_reaction_rules(cobra_model)):
        if rule is not None:
            rxn._gene_reaction_rule = ast2str(gene_renamer.visit(rule))

    for rxn in recompute_reactions:
        rxn.gene_reaction_rule = rxn._gene_reaction_rule
    for i in remove_genes:
        cobra_model.genes.remove(i)