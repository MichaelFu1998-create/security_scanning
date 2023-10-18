def parseSourceURL(source_url):
    ''' Parse the specified version source URL (or version spec), and return an
        instance of VersionSource
    '''
    name, spec = _getNonRegistryRef(source_url)
    if spec:
        return spec

    try:
        url_is_spec = version.Spec(source_url)
    except ValueError:
        url_is_spec = None

    if url_is_spec is not None:
        # if the url is an unadorned version specification (including an empty
        # string) then the source is the module registry:
        return VersionSource('registry', '', source_url)

    raise InvalidVersionSpec("Invalid version specification: \"%s\"" % (source_url))