def _valid_atoms(model, expression):
    """Check whether a sympy expression references the correct variables.

    Parameters
    ----------
    model : cobra.Model
        The model in which to check for variables.
    expression : sympy.Basic
        A sympy expression.

    Returns
    -------
    boolean
        True if all referenced variables are contained in model, False
        otherwise.
    """
    atoms = expression.atoms(optlang.interface.Variable)
    return all(a.problem is model.solver for a in atoms)