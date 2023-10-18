def metabolite_summary(met, solution=None, threshold=0.01, fva=False,
                       names=False, floatfmt='.3g'):
    """
    Print a summary of the production and consumption fluxes.

    This method requires the model for which this metabolite is a part
    to be solved.

    Parameters
    ----------
    solution : cobra.Solution, optional
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
    if solution is None:
        met.model.slim_optimize(error_value=None)
        solution = get_solution(met.model, reactions=met.reactions)

    rxns = sorted(met.reactions, key=attrgetter("id"))
    rxn_id = list()
    rxn_name = list()
    flux = list()
    reaction = list()
    for rxn in rxns:
        rxn_id.append(rxn.id)
        rxn_name.append(format_long_string(emit(rxn), 10))
        flux.append(solution[rxn.id] * rxn.metabolites[met])
        txt = rxn.build_reaction_string(use_metabolite_names=names)
        reaction.append(format_long_string(txt, 40 if fva is not None else 50))

    flux_summary = pd.DataFrame({
        "id": rxn_name,
        "flux": flux,
        "reaction": reaction
    }, index=rxn_id)

    if fva is not None:
        if hasattr(fva, 'columns'):
            fva_results = fva
        else:
            fva_results = flux_variability_analysis(
                met.model, list(met.reactions), fraction_of_optimum=fva)

        flux_summary["maximum"] = zeros(len(rxn_id), dtype=float)
        flux_summary["minimum"] = zeros(len(rxn_id), dtype=float)
        for rxn in rxns:
            fmax = rxn.metabolites[met] * fva_results.at[rxn.id, "maximum"]
            fmin = rxn.metabolites[met] * fva_results.at[rxn.id, "minimum"]
            if abs(fmin) <= abs(fmax):
                flux_summary.at[rxn.id, "fmax"] = fmax
                flux_summary.at[rxn.id, "fmin"] = fmin
            else:
                # Reverse fluxes.
                flux_summary.at[rxn.id, "fmax"] = fmin
                flux_summary.at[rxn.id, "fmin"] = fmax

    assert flux_summary["flux"].sum() < 1E-6, "Error in flux balance"

    flux_summary = _process_flux_dataframe(flux_summary, fva, threshold,
                                           floatfmt)

    flux_summary['percent'] = 0
    total_flux = flux_summary.loc[flux_summary.is_input, "flux"].sum()

    flux_summary.loc[flux_summary.is_input, 'percent'] = \
        flux_summary.loc[flux_summary.is_input, 'flux'] / total_flux
    flux_summary.loc[~flux_summary.is_input, 'percent'] = \
        flux_summary.loc[~flux_summary.is_input, 'flux'] / total_flux

    flux_summary['percent'] = flux_summary.percent.apply(
        lambda x: '{:.0%}'.format(x))

    if fva is not None:
        flux_table = tabulate(
            flux_summary.loc[:, ['percent', 'flux', 'fva_fmt', 'id',
                                 'reaction']].values, floatfmt=floatfmt,
            headers=['%', 'FLUX', 'RANGE', 'RXN ID', 'REACTION']).split('\n')
    else:
        flux_table = tabulate(
            flux_summary.loc[:, ['percent', 'flux', 'id', 'reaction']].values,
            floatfmt=floatfmt, headers=['%', 'FLUX', 'RXN ID', 'REACTION']
        ).split('\n')

    flux_table_head = flux_table[:2]

    met_tag = "{0} ({1})".format(format_long_string(met.name, 45),
                                 format_long_string(met.id, 10))

    head = "PRODUCING REACTIONS -- " + met_tag
    print_(head)
    print_("-" * len(head))
    print_('\n'.join(flux_table_head))
    print_('\n'.join(
        pd.np.array(flux_table[2:])[flux_summary.is_input.values]))

    print_()
    print_("CONSUMING REACTIONS -- " + met_tag)
    print_("-" * len(head))
    print_('\n'.join(flux_table_head))
    print_('\n'.join(
        pd.np.array(flux_table[2:])[~flux_summary.is_input.values]))