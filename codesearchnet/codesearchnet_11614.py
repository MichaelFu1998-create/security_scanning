def satisfyVersion(
        name,
        version_required,
        available,
        search_paths,
        working_directory,
        update_installed=None,
        type='module',  # or 'target'
        inherit_shrinkwrap=None
    ):
    ''' returns a Component/Target for the specified version (either to an already
        installed copy (from the available list, or from disk), or to a newly
        downloaded one), or None if the version could not be satisfied.

        update_installed = None / 'Update'
            None:   prevent any attempt to look for new versions if the
                    component/target already exists
            Update: replace any existing version with the newest available, if
                    the newest available has a higher version
    '''

    r = satisfyFromAvailable(name, available, type=type)
    if r is not None:
        if not sourceparse.parseSourceURL(version_required).semanticSpecMatches(r.getVersion()):
            raise access_common.SpecificationNotMet(
                "Installed %s %s doesn't match specification %s" % (type, name, version_required)
            )
        return r

    r = satisfyVersionFromSearchPaths(
        name,
        version_required,
        search_paths,
        (update_installed == 'Update'),
        type = type,
        inherit_shrinkwrap = inherit_shrinkwrap
    )
    if r is not None:
        return r

    return satisfyVersionByInstalling(
        name, version_required, working_directory, type=type, inherit_shrinkwrap = inherit_shrinkwrap
    )