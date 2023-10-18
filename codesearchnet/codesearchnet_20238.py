def validate(repo, 
             validator_name=None, 
             filename=None, 
             rulesfiles=None,
             args=[]):
    """
    Validate the content of the files for consistency. Validators can
    look as deeply as needed into the files. dgit treats them all as
    black boxes.

    Parameters
    ----------

    repo: Repository object
    validator_name: Name of validator, if any. If none, then all validators specified in dgit.json will be included.
    filename: Pattern that specifies files that must be processed by the validators selected. If none, then the default specification in dgit.json is used.
    rules: Pattern specifying the files that have rules that validators will use
    show: Print the validation results on the terminal

    Returns
    -------

    status: A list of dictionaries, each with target file processed, rules file applied, status of the validation and any error  message.
    """

    mgr = plugins_get_mgr()

    # Expand the specification. Now we have full file paths
    validator_specs = instantiate(repo, validator_name, filename, rulesfiles)

    # Run the validators with rules files...
    allresults = []
    for v in validator_specs:

        keys = mgr.search(what='validator',name=v)['validator']
        for k in keys:
            validator = mgr.get_by_key('validator', k)
            result = validator.evaluate(repo, 
                                        validator_specs[v],
                                        args)
            allresults.extend(result)

    return allresults