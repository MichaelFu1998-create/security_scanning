def reduce_technote_metadata(github_url, metadata, github_data,
                             ltd_product_data):
    """Reduce a technote project's metadata from multiple sources into a
    single JSON-LD resource.

    Parameters
    ----------
    github_url : `str`
        URL of the technote's GitHub repository.
    metadata : `dict`
        The parsed contents of ``metadata.yaml`` found in a technote's
        repository.
    github_data : `dict`
        The contents of the ``technote_repo`` GitHub GraphQL API query.
    ltd_product_data : `dict`
        JSON dataset for the technote corresponding to the
        ``/products/<product>`` of LTD Keeper.

    Returns
    -------
    metadata : `dict`
        JSON-LD-formatted dictionary.

    .. `GitHub personal access token guide`: https://ls.st/41d
    """
    repo_slug = parse_repo_slug_from_url(github_url)

    # Initialize a schema.org/Report and schema.org/SoftwareSourceCode
    # linked data resource
    jsonld = {
        '@context': [
            "https://raw.githubusercontent.com/codemeta/codemeta/2.0-rc/"
            "codemeta.jsonld",
            "http://schema.org"],
        '@type': ['Report', 'SoftwareSourceCode'],
        'codeRepository': github_url
    }

    if 'url' in metadata:
        url = metadata['url']
    elif 'published_url' in ltd_product_data:
        url = ltd_product_data['published_url']
    else:
        raise RuntimeError('No identifying url could be found: '
                           '{}'.format(github_url))
    jsonld['@id'] = url
    jsonld['url'] = url

    if 'series' in metadata and 'serial_number' in metadata:
        jsonld['reportNumber'] = '{series}-{serial_number}'.format(**metadata)
    else:
        raise RuntimeError('No reportNumber: {}'.format(github_url))

    if 'doc_title' in metadata:
        jsonld['name'] = metadata['doc_title']

    if 'description' in metadata:
        jsonld['description'] = metadata['description']

    if 'authors' in metadata:
        jsonld['author'] = [{'@type': 'Person', 'name': author_name}
                            for author_name in metadata['authors']]

    if 'last_revised' in metadata:
        # Prefer getting the 'last_revised' date from metadata.yaml
        # since it's considered an override.
        jsonld['dateModified'] = datetime.datetime.strptime(
            metadata['last_revised'],
            '%Y-%m-%d')
    else:
        # Fallback to parsing the date of the last commit to the
        # default branch on GitHub (usually `master`).
        try:
            _repo_data = github_data['data']['repository']
            _master_data = _repo_data['defaultBranchRef']
            jsonld['dateModified'] = datetime.datetime.strptime(
                _master_data['target']['committedDate'],
                '%Y-%m-%dT%H:%M:%SZ')
        except KeyError:
            pass

    try:
        _license_data = github_data['data']['repository']['licenseInfo']
        _spdxId = _license_data['spdxId']
        if _spdxId is not None:
            _spdx_url = 'https://spdx.org/licenses/{}.html'.format(_spdxId)
            jsonld['license'] = _spdx_url
    except KeyError:
        pass

    try:
        # Find the README(|.md|.rst|*) file in the repo root
        _master_data = github_data['data']['repository']['defaultBranchRef']
        _files = _master_data['target']['tree']['entries']
        for _node in _files:
            filename = _node['name']
            normalized_filename = filename.lower()
            if normalized_filename.startswith('readme'):
                readme_url = make_raw_content_url(repo_slug, 'master',
                                                  filename)
                jsonld['readme'] = readme_url
                break
    except KeyError:
        pass

    # Assume Travis is the CI service (always true at the moment)
    travis_url = 'https://travis-ci.org/{}'.format(repo_slug.full)
    jsonld['contIntegration'] = travis_url

    return jsonld