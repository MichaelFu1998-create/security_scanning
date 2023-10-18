def remoteComponentFor(name, version_required, registry='modules'):
    ''' Return a RemoteComponent sublclass for the specified component name and
        source url (or version specification)
        Raises an exception if any arguments are invalid.
    '''

    try:
        vs = sourceparse.parseSourceURL(version_required)
    except ValueError as e:
        raise access_common.Unavailable(
            '%s' % (e)
        )

    if vs.source_type == 'registry':
        if registry not in ('modules', 'targets'):
            raise Exception('no known registry namespace "%s"' % registry)
        return registry_access.RegistryThing.createFromSource(
            vs, name, registry=registry
        )
    elif vs.source_type == 'github':
        return github_access.GithubComponent.createFromSource(vs, name)
    elif vs.source_type == 'git':
        return git_access.GitComponent.createFromSource(vs, name)
    elif vs.source_type == 'hg':
        return hg_access.HGComponent.createFromSource(vs, name)
    else:
        raise Exception('unsupported module source: "%s"' % vs.source_type)