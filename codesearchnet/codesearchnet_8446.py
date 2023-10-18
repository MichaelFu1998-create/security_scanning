def paths_from_env(prefix=None, names=None):
    """Construct dict of paths from environment variables'"""


    def expand_path(path):
        """Expands variables in 'path' and turns it into absolute path"""

        return os.path.abspath(os.path.expanduser(os.path.expandvars(path)))


    if prefix is None:
        prefix = "CIJ"
    if names is None:
        names = [
            "ROOT", "ENVS", "TESTPLANS", "TESTCASES", "TESTSUITES", "MODULES",
            "HOOKS", "TEMPLATES"
        ]

    conf = {v: os.environ.get("_".join([prefix, v])) for v in names}

    for env in (e for e in conf.keys() if e[:len(prefix)] in names and conf[e]):
        conf[env] = expand_path(conf[env])
        if not os.path.exists(conf[env]):
            err("%s_%s: %r, does not exist" % (prefix, env, conf[env]))

    return conf