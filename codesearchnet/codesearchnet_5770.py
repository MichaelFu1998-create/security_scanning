def get(http, path, root=METADATA_ROOT, recursive=None):
    """Fetch a resource from the metadata server.

    Args:
        http: an object to be used to make HTTP requests.
        path: A string indicating the resource to retrieve. For example,
            'instance/service-accounts/default'
        root: A string indicating the full path to the metadata server root.
        recursive: A boolean indicating whether to do a recursive query of
            metadata. See
            https://cloud.google.com/compute/docs/metadata#aggcontents

    Returns:
        A dictionary if the metadata server returns JSON, otherwise a string.

    Raises:
        http_client.HTTPException if an error corrured while
        retrieving metadata.
    """
    url = urlparse.urljoin(root, path)
    url = _helpers._add_query_parameter(url, 'recursive', recursive)

    response, content = transport.request(
        http, url, headers=METADATA_HEADERS)

    if response.status == http_client.OK:
        decoded = _helpers._from_bytes(content)
        if response['content-type'] == 'application/json':
            return json.loads(decoded)
        else:
            return decoded
    else:
        raise http_client.HTTPException(
            'Failed to retrieve {0} from the Google Compute Engine'
            'metadata service. Response:\n{1}'.format(url, response))