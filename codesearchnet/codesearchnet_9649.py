def path_exists(path):
    """
    Check if file exists either remote or local.

    Parameters:
    -----------
    path : path to file

    Returns:
    --------
    exists : bool
    """
    if path.startswith(("http://", "https://")):
        try:
            urlopen(path).info()
            return True
        except HTTPError as e:
            if e.code == 404:
                return False
            else:
                raise
    elif path.startswith("s3://"):
        bucket = get_boto3_bucket(path.split("/")[2])
        key = "/".join(path.split("/")[3:])
        for obj in bucket.objects.filter(Prefix=key):
            if obj.key == key:
                return True
        else:
            return False
    else:
        logger.debug("%s exists: %s", path, os.path.exists(path))
        return os.path.exists(path)