def _bqm_from_1sat(constraint):
    """create a bqm for a constraint with only one variable

    bqm will have exactly classical gap 2.
    """
    configurations = constraint.configurations
    num_configurations = len(configurations)

    bqm = dimod.BinaryQuadraticModel.empty(constraint.vartype)

    if num_configurations == 1:
        val, = next(iter(configurations))
        v, = constraint.variables
        bqm.add_variable(v, -1 if val > 0 else +1, vartype=dimod.SPIN)
    else:
        bqm.add_variables_from((v, 0.0) for v in constraint.variables)

    return bqm