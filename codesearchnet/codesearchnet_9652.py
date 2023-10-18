def write_json(path, params):
    """Write local or remote."""
    logger.debug("write %s to %s", params, path)
    if path.startswith("s3://"):
        bucket = get_boto3_bucket(path.split("/")[2])
        key = "/".join(path.split("/")[3:])
        logger.debug("upload %s", key)
        bucket.put_object(
            Key=key,
            Body=json.dumps(params, sort_keys=True, indent=4)
        )
    else:
        makedirs(os.path.dirname(path))
        with open(path, 'w') as dst:
            json.dump(params, dst, sort_keys=True, indent=4)