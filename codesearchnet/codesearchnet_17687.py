def _create_air():
    """
    Create a dictionary of datasets and a material object for air.

    :return: (Material, {str, DataSet})
    """
    name = "Air"
    namel = name.lower()
    mm = 28.9645  # g/mol

    ds_dict = _create_ds_dict([
        "dataset-air-lienhard2015",
        "dataset-air-lienhard2018"])
    active_ds = "dataset-air-lienhard2018"

    # create polynomial models to describe material properties
    #   comment it out after model creation is complete, so that it does not
    #   run every time during use.
    # _create_polynomial_model(name, "Cp", 13, ds_dict[active_ds], ds_dict)
    # _create_polynomial_model(name, "k", 8, ds_dict[active_ds], ds_dict)
    # _create_polynomial_model(name, "mu", 8, ds_dict[active_ds], ds_dict)
    # _create_polynomial_model(name, "rho", 14, ds_dict[active_ds], ds_dict)

    # IgRhoT(mm, 101325.0).plot(ds_dict, _path(f"data/{namel}-rho-igrhot.pdf"))

    model_dict = {
        "rho": IgRhoT(mm, 101325.0),
        "beta": IgBetaT()}

    model_type = "polynomialmodelt"
    for property in ["Cp", "mu", "k"]:
        name = f"data/{namel}-{property.lower()}-{model_type}-{active_ds}.json"
        model_dict[property] = PolynomialModelT.read(_path(name))

    material = Material(name, StateOfMatter.gas, model_dict)

    return material, ds_dict