def list_objects_in_bucket(**kwargs):
    """
    List objects in bucket.

    :param Bucket: name of bucket
    :type Bucket: ``str``

    :returns list of objects in bucket
    :rtype: ``list``
    """
    bucket = get_bucket(**kwargs)
    if bucket:
        return [o for o in bucket.list_blobs()]
    else:
        return None