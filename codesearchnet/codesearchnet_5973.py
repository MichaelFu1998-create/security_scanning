def list_buckets(client=None, **kwargs):
    """
    List buckets for a project.

    :param client: client object to use.
    :type client: Google Cloud Storage client

    :returns: list of dictionary reprsentation of Bucket
    :rtype: ``list`` of ``dict``
    """
    buckets = client.list_buckets(**kwargs)
    return [b.__dict__ for b in buckets]