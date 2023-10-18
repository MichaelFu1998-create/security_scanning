def itertable(table):
    """Auxiliary function for iterating over a data table."""
    for item in table:
        res = {
            k.lower(): nfd(v) if isinstance(v, text_type) else v for k, v in item.items()}
        for extra in res.pop('extra', []):
            k, _, v = extra.partition(':')
            res[k.strip()] = v.strip()
        yield res