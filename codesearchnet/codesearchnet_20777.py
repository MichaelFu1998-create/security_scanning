def reader(ltsvfile, labels=None):
    """Make LTSV Reader for reading selected labels.

    :param  ltsvfile: iterable of lines.
    :param  labels: sequence of labels. (optional)
    :return: generator of record in [[label, value], ...] form.
    """
    label_pattern = re.compile(r"^[0-9A-Za-z_.-]+:")

    if labels is not None:
        prefixes = tuple(L + ':' for L in labels
                if label_pattern.match(L + ':'))
        for record in ltsvfile:
            record = record.rstrip('\r\n')
            yield [x.split(':', 1) for x in record.split('\t')
                    if x.startswith(prefixes)]
        return

    for record in ltsvfile:
        record = record.rstrip('\r\n')
        yield [x.split(':', 1) for x in record.split('\t')
                if label_pattern.match(x)]