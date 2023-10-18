def model_summary(model, solution=None, threshold=0.01, fva=None, names=False,
                  floatfmt='.3g'):
    """
    Print a summary of the input and output fluxes of the model.

    Parameters
    ----------
    solution: cobra.Solution, optional
        A previously solved model solution to use for generating the
        summary. If none provided (default), the summary method will
        resolve the model. Note that the solution object must match the
        model, i.e., changes to the model such as changed bounds,
        added or removed reactions are not taken into account by this
        method.
    threshold : float, optional
        Threshold below which fluxes are not reported.
    fva : pandas.DataFrame, float or None, optional
        Whether or not to include flux variability analysis in the output.
        If given, fva should either be a previous FVA solution matching
        the model or a float between 0 and 1 representing the
        fraction of the optimum objective to be searched.
    names : bool, optional
        Emit reaction and metabolite names rather than identifiers (default
        False).
    floatfmt : string, optional
        Format string for floats (default '.3g').

    """
    if names:
        emit = attrgetter('name')
    else:
        emit = attrgetter('id')
    objective_reactions = linear_reaction_coefficients(model)
    boundary_reactions = model.exchanges
    summary_rxns = set(objective_reactions.keys()).union(boundary_reactions)

    if solution is None:
        model.slim_optimize(error_value=None)
        solution = get_solution(model, reactions=summary_rxns)

    # Create a dataframe of objective fluxes
    obj_fluxes = pd.DataFrame({key: solution[key.id] * value for key,
                               value in iteritems(objective_reactions)},
                              index=['flux']).T
    obj_fluxes['id'] = obj_fluxes.apply(
        lambda x: format_long_string(x.name.id, 15), 1)

    # Build a dictionary of metabolite production from the boundary reactions
    metabolites = {m for r in boundary_reactions for m in r.metabolites}
    index = sorted(metabolites, key=attrgetter('id'))
    metabolite_fluxes = pd.DataFrame({
        'id': [format_long_string(emit(m), 15) for m in index],
        'flux': zeros(len(index), dtype=float)
    }, index=[m.id for m in index])
    for rxn in boundary_reactions:
        for met, stoich in iteritems(rxn.metabolites):
            metabolite_fluxes.at[met.id, 'flux'] += stoich * solution[rxn.id]

    # Calculate FVA results if requested
    if fva is not None:
        if len(index) != len(boundary_reactions):
            LOGGER.warning(
                "There exists more than one boundary reaction per metabolite. "
                "Please be careful when evaluating flux ranges.")
        metabolite_fluxes['fmin'] = zeros(len(index), dtype=float)
        metabolite_fluxes['fmax'] = zeros(len(index), dtype=float)
        if hasattr(fva, 'columns'):
            fva_results = fva
        else:
            fva_results = flux_variability_analysis(
                model, reaction_list=boundary_reactions,
                fraction_of_optimum=fva)

        for rxn in boundary_reactions:
            for met, stoich in iteritems(rxn.metabolites):
                fmin = stoich * fva_results.at[rxn.id, 'minimum']
                fmax = stoich * fva_results.at[rxn.id, 'maximum']
                # Correct 'max' and 'min' for negative values
                if abs(fmin) <= abs(fmax):
                    metabolite_fluxes.at[met.id, 'fmin'] += fmin
                    metabolite_fluxes.at[met.id, 'fmax'] += fmax
                else:
                    metabolite_fluxes.at[met.id, 'fmin'] += fmax
                    metabolite_fluxes.at[met.id, 'fmax'] += fmin

    # Generate a dataframe of boundary fluxes
    metabolite_fluxes = _process_flux_dataframe(
        metabolite_fluxes, fva, threshold, floatfmt)

    # Begin building string output table
    def get_str_table(species_df, fva=False):
        """Formats a string table for each column"""
        if fva:
            return tabulate(
                species_df.loc[:, ['id', 'flux', 'fva_fmt']].values,
                floatfmt=floatfmt, tablefmt='simple',
                headers=['id', 'Flux', 'Range']).split('\n')
        else:
            return tabulate(species_df.loc[:, ['id', 'flux']].values,
                            floatfmt=floatfmt, tablefmt='plain').split('\n')

    in_table = get_str_table(
        metabolite_fluxes[metabolite_fluxes['is_input']], fva=fva is not None)
    out_table = get_str_table(
        metabolite_fluxes[~metabolite_fluxes['is_input']], fva=fva is not None)
    obj_table = get_str_table(obj_fluxes, fva=False)

    # Print nested output table
    print_(tabulate(
        [entries for entries in zip_longest(in_table, out_table, obj_table)],
        headers=['IN FLUXES', 'OUT FLUXES', 'OBJECTIVES'], tablefmt='simple'))