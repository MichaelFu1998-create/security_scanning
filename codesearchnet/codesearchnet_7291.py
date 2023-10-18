def resolve(cls, all_known_repos, name):
        """We require the list of all remote repo paths to be passed in
        to this because otherwise we would need to import the spec assembler
        in this module, which would give us circular imports."""
        match = None
        for repo in all_known_repos:
            if repo.remote_path == name: # user passed in a full name
                return repo
            if name == repo.short_name:
                if match is None:
                    match = repo
                else:
                    raise RuntimeError('Short repo name {} is ambiguous. It matches both {} and {}'.format(name,
                                                                                                           match.remote_path,
                                                                                                           repo.remote_path))
        if match is None:
            raise RuntimeError('Short repo name {} does not match any known repos'.format(name))
        return match