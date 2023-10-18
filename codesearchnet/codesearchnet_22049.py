def open_s3(bucket):
    """
    Opens connection to S3 returning bucket and key
    """
    conn = boto.connect_s3(options.paved.s3.access_id, options.paved.s3.secret)
    try:
        bucket = conn.get_bucket(bucket)
    except boto.exception.S3ResponseError:
        bucket = conn.create_bucket(bucket)
    return bucket