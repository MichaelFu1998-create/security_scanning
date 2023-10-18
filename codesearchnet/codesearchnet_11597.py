def publish(namespace, name, version, description_file, tar_file, readme_file,
            readme_file_ext, registry=None):
    ''' Publish a tarblob to the registry, if the request fails, an exception
        is raised, which either triggers re-authentication, or is turned into a
        return value by the decorators. (If successful, the decorated function
        returns None)
    '''
    registry = registry or Registry_Base_URL

    url = '%s/%s/%s/versions/%s' % (
        registry,
        namespace,
        name,
        version
    )

    if readme_file_ext == '.md':
        readme_section_name = 'readme.md'
    elif readme_file_ext == '':
        readme_section_name = 'readme'
    else:
        raise ValueError('unsupported readme type: "%s"' % readme_file_ext)

    # description file is in place as text (so read it), tar file is a file
    body = OrderedDict([('metadata', (None, description_file.read(),'application/json')),
                        ('tarball',('tarball', tar_file)),
                        (readme_section_name, (readme_section_name, readme_file))])

    headers = _headersForRegistry(registry)

    response = requests.put(url, headers=headers, files=body)
    response.raise_for_status()

    return None