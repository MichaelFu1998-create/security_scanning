def fields_checker(fields):
    """
    returns a fields argument formatted as a list of strings.
    and doesn't allow zero.
    """
    ## make sure fields will work
    if isinstance(fields, int):
        fields = str(fields)
    if isinstance(fields, str):
        if "," in fields:
            fields = [str(i) for i in fields.split(",")]
        else:
            fields = [str(fields)]
    elif isinstance(fields, (tuple, list)):
        fields = [str(i) for i in fields]
    else:
        raise IPyradWarningExit("fields not properly formatted")

    ## do not allow zero in fields
    fields = [i for i in fields if i != '0']

    return fields