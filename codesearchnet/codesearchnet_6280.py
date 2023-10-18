def save_matlab_model(model, file_name, varname=None):
    """Save the cobra model as a .mat file.

    This .mat file can be used directly in the MATLAB version of COBRA.

    Parameters
    ----------
    model : cobra.core.Model.Model object
        The model to save
    file_name : str or file-like object
        The file to save to
    varname : string
       The name of the variable within the workspace
    """
    if not scipy_io:
        raise ImportError('load_matlab_model requires scipy')

    if varname is None:
        varname = str(model.id) \
            if model.id is not None and len(model.id) > 0 \
            else "exported_model"
    mat = create_mat_dict(model)
    scipy_io.savemat(file_name, {varname: mat},
                     appendmat=True, oned_as="column")