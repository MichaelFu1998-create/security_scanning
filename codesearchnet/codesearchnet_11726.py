def get_selections():
    """
    Get the state of ``dkpg`` selections.

    Returns a dict with state => [packages].
    """
    with settings(hide('stdout')):
        res = run_as_root('dpkg --get-selections')
    selections = dict()
    for line in res.splitlines():
        package, status = line.split()
        selections.setdefault(status, list()).append(package)
    return selections