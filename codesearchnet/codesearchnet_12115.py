def _get_value(quantitystr, fitparams, fixedparams):
    """This decides if a value is to be fit for or is fixed in a model fit.

    When you want to get the value of some parameter, but you're not sure if
    it's being fit or if it is fixed. then, e.g. for `period`::

        period_value = _get_value('period', fitparams, fixedparams)

    """

    # for Mandel-Agol fitting, sometimes we want to fix some parameters,
    # and fit others. this function allows that flexibility.
    fitparamskeys, fixedparamskeys = fitparams.keys(), fixedparams.keys()
    if quantitystr in fitparamskeys:
        quantity = fitparams[quantitystr]
    elif quantitystr in fixedparamskeys:
        quantity = fixedparams[quantitystr]
    return quantity