def _mdp_include_string(dirs):
    """Generate a string that can be added to a mdp 'include = ' line."""
    include_paths = [os.path.expanduser(p) for p in dirs]
    return ' -I'.join([''] + include_paths)