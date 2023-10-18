def assert_optimal(model, message='optimization failed'):
    """Assert model solver status is optimal.

    Do nothing if model solver status is optimal, otherwise throw
    appropriate exception depending on the status.

    Parameters
    ----------
    model : cobra.Model
        The model to check the solver status for.
    message : str (optional)
        Message to for the exception if solver status was not optimal.
    """
    status = model.solver.status
    if status != OPTIMAL:
        exception_cls = OPTLANG_TO_EXCEPTIONS_DICT.get(
            status, OptimizationError)
        raise exception_cls("{} ({})".format(message, status))