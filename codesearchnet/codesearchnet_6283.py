def model_to_pymatbridge(model, variable_name="model", matlab=None):
    """send the model to a MATLAB workspace through pymatbridge

    This model can then be manipulated through the COBRA toolbox

    Parameters
    ----------
    variable_name : str
        The variable name to which the model will be assigned in the
        MATLAB workspace

    matlab : None or pymatbridge.Matlab instance
        The MATLAB workspace to which the variable will be sent. If
        this is None, then this will be sent to the same environment
        used in IPython magics.

    """
    if scipy_sparse is None:
        raise ImportError("`model_to_pymatbridge` requires scipy!")
    if matlab is None:  # assumed to be running an IPython magic
        from IPython import get_ipython
        matlab = get_ipython().magics_manager.registry["MatlabMagics"].Matlab
    model_info = create_mat_dict(model)
    S = model_info["S"].todok()
    model_info["S"] = 0
    temp_S_name = "cobra_pymatbridge_temp_" + uuid4().hex
    _check(matlab.set_variable(variable_name, model_info))
    _check(matlab.set_variable(temp_S_name, S))
    _check(matlab.run_code("%s.S = %s;" % (variable_name, temp_S_name)))
    # all vectors need to be transposed
    for i in model_info.keys():
        if i == "S":
            continue
        _check(matlab.run_code("{0}.{1} = {0}.{1}';".format(variable_name, i)))
    _check(matlab.run_code("clear %s;" % temp_S_name))