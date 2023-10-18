def DictReader(ltsvfile, labels=None, dict_type=dict):
    """Make LTSV Reader for reading selected labels.

    :param  ltsvfile: iterable of lines.
    :param  labels: sequence of labels.
    :return: generator of record in {label: value, ...} form.
    """
    for rec in reader(ltsvfile, labels):
        yield dict_type(rec)