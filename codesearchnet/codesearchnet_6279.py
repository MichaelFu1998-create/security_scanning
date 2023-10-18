def load_matlab_model(infile_path, variable_name=None, inf=inf):
    """Load a cobra model stored as a .mat file

    Parameters
    ----------
    infile_path: str
        path to the file to to read
    variable_name: str, optional
        The variable name of the model in the .mat file. If this is not
        specified, then the first MATLAB variable which looks like a COBRA
        model will be used
    inf: value
        The value to use for infinite bounds. Some solvers do not handle
        infinite values so for using those, set this to a high numeric value.

    Returns
    -------
    cobra.core.Model.Model:
        The resulting cobra model

    """
    if not scipy_io:
        raise ImportError('load_matlab_model requires scipy')

    data = scipy_io.loadmat(infile_path)
    possible_names = []
    if variable_name is None:
        # skip meta variables
        meta_vars = {"__globals__", "__header__", "__version__"}
        possible_names = sorted(i for i in data if i not in meta_vars)
        if len(possible_names) == 1:
            variable_name = possible_names[0]
    if variable_name is not None:
        return from_mat_struct(data[variable_name], model_id=variable_name,
                               inf=inf)
    for possible_name in possible_names:
        try:
            return from_mat_struct(data[possible_name], model_id=possible_name,
                                   inf=inf)
        except ValueError:
            pass
    # If code here is executed, then no model was found.
    raise IOError("no COBRA model found")