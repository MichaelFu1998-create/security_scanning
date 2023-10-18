def assess_component(model, reaction, side, flux_coefficient_cutoff=0.001,
                     solver=None):
    """Assesses the ability of the model to provide sufficient precursors,
    or absorb products, for a reaction operating at, or beyond,
    the specified cutoff.

    Parameters
    ----------
    model : cobra.Model
        The cobra model to assess production capacity for

    reaction : reaction identifier or cobra.Reaction
        The reaction to assess

    side : basestring
        Side of the reaction, 'products' or 'reactants'

    flux_coefficient_cutoff :  float
        The minimum flux that reaction must carry to be considered active.

    solver : basestring
        Solver name. If None, the default solver will be used.

    Returns
    -------
    bool or dict
        True if the precursors can be simultaneously produced at the
        specified cutoff. False, if the model has the capacity to produce
        each individual precursor at the specified threshold  but not all
        precursors at the required level simultaneously. Otherwise a
        dictionary of the required and the produced fluxes for each reactant
        that is not produced in sufficient quantities.

    """
    reaction = model.reactions.get_by_any(reaction)[0]
    result_key = dict(reactants='produced', products='capacity')[side]
    get_components = attrgetter(side)
    with model as m:
        m.objective = reaction
        if _optimize_or_value(m, solver=solver) >= flux_coefficient_cutoff:
            return True
        simulation_results = {}
        # build the demand reactions and add all at once
        demand_reactions = {}
        for component in get_components(reaction):
            coeff = reaction.metabolites[component]
            demand = m.add_boundary(component, type='demand')
            demand.metabolites[component] = coeff
            demand_reactions[demand] = (component, coeff)
        # First assess whether all precursors can be produced simultaneously
        joint_demand = Reaction("joint_demand")
        for demand_reaction in demand_reactions:
            joint_demand += demand_reaction
        m.add_reactions([joint_demand])
        m.objective = joint_demand
        if _optimize_or_value(m, solver=solver) >= flux_coefficient_cutoff:
            return True

        # Otherwise assess the ability of the model to produce each precursor
        # individually.  Now assess the ability of the model to produce each
        # reactant for a reaction
        for demand_reaction, (component, coeff) in iteritems(demand_reactions):
            # Calculate the maximum amount of the
            with m:
                m.objective = demand_reaction
                flux = _optimize_or_value(m, solver=solver)
            # metabolite that can be produced.
            if flux_coefficient_cutoff > flux:
                # Scale the results to a single unit
                simulation_results.update({
                    component: {
                        'required': flux_coefficient_cutoff / abs(coeff),
                        result_key: flux / abs(coeff)
                    }})
        if len(simulation_results) == 0:
            simulation_results = False
        return simulation_results