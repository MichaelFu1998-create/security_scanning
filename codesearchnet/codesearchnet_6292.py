def add_boundary(self, metabolite, type="exchange", reaction_id=None,
                     lb=None, ub=None, sbo_term=None):
        """
        Add a boundary reaction for a given metabolite.

        There are three different types of pre-defined boundary reactions:
        exchange, demand, and sink reactions.
        An exchange reaction is a reversible, unbalanced reaction that adds
        to or removes an extracellular metabolite from the extracellular
        compartment.
        A demand reaction is an irreversible reaction that consumes an
        intracellular metabolite.
        A sink is similar to an exchange but specifically for intracellular
        metabolites.

        If you set the reaction `type` to something else, you must specify the
        desired identifier of the created reaction along with its upper and
        lower bound. The name will be given by the metabolite name and the
        given `type`.

        Parameters
        ----------
        metabolite : cobra.Metabolite
            Any given metabolite. The compartment is not checked but you are
            encouraged to stick to the definition of exchanges and sinks.
        type : str, {"exchange", "demand", "sink"}
            Using one of the pre-defined reaction types is easiest. If you
            want to create your own kind of boundary reaction choose
            any other string, e.g., 'my-boundary'.
        reaction_id : str, optional
            The ID of the resulting reaction. This takes precedence over the
            auto-generated identifiers but beware that it might make boundary
            reactions harder to identify afterwards when using `model.boundary`
            or specifically `model.exchanges` etc.
        lb : float, optional
            The lower bound of the resulting reaction.
        ub : float, optional
            The upper bound of the resulting reaction.
        sbo_term : str, optional
            A correct SBO term is set for the available types. If a custom
            type is chosen, a suitable SBO term should also be set.

        Returns
        -------
        cobra.Reaction
            The created boundary reaction.

        Examples
        --------
        >>> import cobra.test
        >>> model = cobra.test.create_test_model("textbook")
        >>> demand = model.add_boundary(model.metabolites.atp_c, type="demand")
        >>> demand.id
        'DM_atp_c'
        >>> demand.name
        'ATP demand'
        >>> demand.bounds
        (0, 1000.0)
        >>> demand.build_reaction_string()
        'atp_c --> '

        """
        ub = CONFIGURATION.upper_bound if ub is None else ub
        lb = CONFIGURATION.lower_bound if lb is None else lb
        types = {
            "exchange": ("EX", lb, ub, sbo_terms["exchange"]),
            "demand": ("DM", 0, ub, sbo_terms["demand"]),
            "sink": ("SK", lb, ub, sbo_terms["sink"])
        }
        if type == "exchange":
            external = find_external_compartment(self)
            if metabolite.compartment != external:
                raise ValueError("The metabolite is not an external metabolite"
                                 " (compartment is `%s` but should be `%s`). "
                                 "Did you mean to add a demand or sink? "
                                 "If not, either change its compartment or "
                                 "rename the model compartments to fix this." %
                                 (metabolite.compartment, external))
        if type in types:
            prefix, lb, ub, default_term = types[type]
            if reaction_id is None:
                reaction_id = "{}_{}".format(prefix, metabolite.id)
            if sbo_term is None:
                sbo_term = default_term
        if reaction_id is None:
            raise ValueError(
                "Custom types of boundary reactions require a custom "
                "identifier. Please set the `reaction_id`.")
        if reaction_id in self.reactions:
            raise ValueError(
                "Boundary reaction '{}' already exists.".format(reaction_id))
        name = "{} {}".format(metabolite.name, type)
        rxn = Reaction(id=reaction_id, name=name, lower_bound=lb,
                       upper_bound=ub)
        rxn.add_metabolites({metabolite: -1})
        if sbo_term:
            rxn.annotation["sbo"] = sbo_term
        self.add_reactions([rxn])
        return rxn