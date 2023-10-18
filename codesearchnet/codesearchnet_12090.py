def checkplot_infokey_worker(task):
    '''This gets the required keys from the requested file.

    Parameters
    ----------

    task : tuple
        Task is a two element tuple::

        - task[0] is the dict to work on

        - task[1] is a list of lists of str indicating all the key address to
          extract items from the dict for

    Returns
    -------

    list
        This is a list of all of the items at the requested key addresses.

    '''
    cpf, keys = task

    cpd = _read_checkplot_picklefile(cpf)

    resultkeys = []

    for k in keys:

        try:
            resultkeys.append(_dict_get(cpd, k))
        except Exception as e:
            resultkeys.append(np.nan)

    return resultkeys