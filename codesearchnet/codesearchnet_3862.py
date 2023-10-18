def parse_requirements_alt(fname='requirements.txt'):
    """
    pip install requirements-parser
    fname='requirements.txt'
    """
    import requirements
    from os.path import dirname, join, exists
    require_fpath = join(dirname(__file__), fname)
    if exists(require_fpath):
        # Dont use until this handles platform specific dependencies
        with open(require_fpath, 'r') as file:
            requires = list(requirements.parse(file))
        packages = [r.name for r in requires]
        return packages
    return []