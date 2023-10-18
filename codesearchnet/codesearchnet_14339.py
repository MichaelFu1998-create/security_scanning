def _format(formatter, x):
    """
    Helper to format and tidy up
    """
    # For MPL to play nice
    formatter.create_dummy_axis()
    # For sensible decimal places
    formatter.set_locs([val for val in x if ~np.isnan(val)])
    try:
        oom = int(formatter.orderOfMagnitude)
    except AttributeError:
        oom = 0
    labels = [formatter(tick) for tick in x]

    # Remove unnecessary decimals
    pattern = re.compile(r'\.0+$')
    for i, label in enumerate(labels):
        match = pattern.search(label)
        if match:
            labels[i] = pattern.sub('', label)

    # MPL does not add the exponential component
    if oom:
        labels = ['{}e{}'.format(s, oom) if s != '0' else s
                  for s in labels]
    return labels