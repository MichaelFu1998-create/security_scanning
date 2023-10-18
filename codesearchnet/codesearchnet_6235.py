def check_solver_status(status, raise_error=False):
    """Perform standard checks on a solver's status."""
    if status == OPTIMAL:
        return
    elif (status in has_primals) and not raise_error:
        warn("solver status is '{}'".format(status), UserWarning)
    elif status is None:
        raise OptimizationError(
            "model was not optimized yet or solver context switched")
    else:
        raise OptimizationError("solver status is '{}'".format(status))