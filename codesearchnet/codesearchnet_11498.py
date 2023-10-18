def _bqm_from_2sat(constraint):
    """create a bqm for a constraint with two variables.

    bqm will have exactly classical gap 2.
    """
    configurations = constraint.configurations
    variables = constraint.variables
    vartype = constraint.vartype
    u, v = constraint.variables

    # if all configurations are present, then nothing is infeasible and the bqm is just all
    # 0.0s
    if len(configurations) == 4:
        return dimod.BinaryQuadraticModel.empty(constraint.vartype)

    # check if the constraint is irreducible, and if so, build the bqm for its two
    # components
    components = irreducible_components(constraint)
    if len(components) > 1:
        const0 = Constraint.from_configurations(((config[0],) for config in configurations),
                                                (u,), vartype)
        const1 = Constraint.from_configurations(((config[1],) for config in configurations),
                                                (v,), vartype)
        bqm = _bqm_from_1sat(const0)
        bqm.update(_bqm_from_1sat(const1))
        return bqm

    assert len(configurations) > 1, "single configurations should be irreducible"

    # if it is not irreducible, and there are infeasible configurations, then it is time to
    # start building a bqm
    bqm = dimod.BinaryQuadraticModel.empty(vartype)

    # if the constraint is not irreducible and has two configurations, then it is either eq or ne
    if all(operator.eq(*config) for config in configurations):
        bqm.add_interaction(u, v, -1, vartype=dimod.SPIN)  # equality
    elif all(operator.ne(*config) for config in configurations):
        bqm.add_interaction(u, v, +1, vartype=dimod.SPIN)  # inequality
    elif (1, 1) not in configurations:
        bqm.add_interaction(u, v, 2, vartype=dimod.BINARY)  # penalize (1, 1)
    elif (-1, +1) not in configurations and (0, 1) not in configurations:
        bqm.add_interaction(u, v, -2, vartype=dimod.BINARY)
        bqm.add_variable(v, 2, vartype=dimod.BINARY)
    elif (+1, -1) not in configurations and (1, 0) not in configurations:
        bqm.add_interaction(u, v, -2, vartype=dimod.BINARY)
        bqm.add_variable(u, 2, vartype=dimod.BINARY)
    else:
        # (0, 0) not in configurations
        bqm.add_interaction(u, v, 2, vartype=dimod.BINARY)
        bqm.add_variable(u, -2, vartype=dimod.BINARY)
        bqm.add_variable(v, -2, vartype=dimod.BINARY)

    return bqm