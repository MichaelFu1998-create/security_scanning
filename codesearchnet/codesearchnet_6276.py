def model_from_dict(obj):
    """Build a model from a dict.

    Models stored in json are first formulated as a dict that can be read to
    cobra model using this function.

    Parameters
    ----------
    obj : dict
        A dictionary with elements, 'genes', 'compartments', 'id',
        'metabolites', 'notes' and 'reactions'; where 'metabolites', 'genes'
        and 'metabolites' are in turn lists with dictionaries holding all
        attributes to form the corresponding object.

    Returns
    -------
    cora.core.Model
        The generated model.

    See Also
    --------
    cobra.io.model_to_dict
    """
    if 'reactions' not in obj:
        raise ValueError('Object has no reactions attribute. Cannot load.')
    model = Model()
    model.add_metabolites(
        [metabolite_from_dict(metabolite) for metabolite in obj['metabolites']]
    )
    model.genes.extend([gene_from_dict(gene) for gene in obj['genes']])
    model.add_reactions(
        [reaction_from_dict(reaction, model) for reaction in obj['reactions']]
    )
    objective_reactions = [rxn for rxn in obj['reactions'] if
                           rxn.get('objective_coefficient', 0) != 0]
    coefficients = {
        model.reactions.get_by_id(rxn['id']): rxn['objective_coefficient'] for
        rxn in objective_reactions}
    set_objective(model, coefficients)
    for k, v in iteritems(obj):
        if k in {'id', 'name', 'notes', 'compartments', 'annotation'}:
            setattr(model, k, v)
    return model