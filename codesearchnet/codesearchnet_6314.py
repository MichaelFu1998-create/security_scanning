def _init_worker(model, loopless, sense):
    """Initialize a global model object for multiprocessing."""
    global _model
    global _loopless
    _model = model
    _model.solver.objective.direction = sense
    _loopless = loopless