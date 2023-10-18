def read_json(path):
    """Read local or remote."""
    if path.startswith(("http://", "https://")):
        try:
            return json.loads(urlopen(path).read().decode())
        except HTTPError:
            raise FileNotFoundError("%s not found", path)
    elif path.startswith("s3://"):
        bucket = get_boto3_bucket(path.split("/")[2])
        key = "/".join(path.split("/")[3:])
        for obj in bucket.objects.filter(Prefix=key):
            if obj.key == key:
                return json.loads(obj.get()['Body'].read().decode())
        raise FileNotFoundError("%s not found", path)
    else:
        try:
            with open(path, "r") as src:
                return json.loads(src.read())
        except:
            raise FileNotFoundError("%s not found", path)