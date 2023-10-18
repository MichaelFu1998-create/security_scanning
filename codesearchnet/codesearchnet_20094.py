def stats(args):
    """
    cldf stats <DATASET>

    Print basic stats for CLDF dataset <DATASET>, where <DATASET> may be the path to
    - a CLDF metadata file
    - a CLDF core data file
    """
    ds = _get_dataset(args)
    print(ds)
    md = Table('key', 'value')
    md.extend(ds.properties.items())
    print(md.render(condensed=False, tablefmt=None))
    print()
    t = Table('Path', 'Type', 'Rows')
    for p, type_, r in ds.stats():
        t.append([p, type_, r])
    print(t.render(condensed=False, tablefmt=None))