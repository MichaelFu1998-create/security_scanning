def _create_polynomial_model(
    name: str,
    symbol: str,
    degree: int,
    ds: DataSet,
    dss: dict):
    """
    Create a polynomial model to describe the specified property based on the
    specified data set, and save it to a .json file.

    :param name: material name.
    :param symbol: property symbol.
    :param degree: polynomial degree.
    :param ds: the source data set.
    :param dss: dictionary of all datasets.
    """
    ds_name = ds.name.split(".")[0].lower()
    file_name = f"{name.lower()}-{symbol.lower()}-polynomialmodelt-{ds_name}"
    newmod = PolynomialModelT.create(ds, symbol, degree)
    newmod.plot(dss, _path(f"data/{file_name}.pdf"), False)
    newmod.write(_path(f"data/{file_name}.json"))