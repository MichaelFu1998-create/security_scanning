def upload_s3(cfg, path_to_zip_file, *use_s3):
    """Upload a function to AWS S3."""

    print('Uploading your new Lambda function')
    profile_name = cfg.get('profile')
    aws_access_key_id = cfg.get('aws_access_key_id')
    aws_secret_access_key = cfg.get('aws_secret_access_key')
    client = get_client(
        's3', profile_name, aws_access_key_id, aws_secret_access_key,
        cfg.get('region'),
    )
    byte_stream = b''
    with open(path_to_zip_file, mode='rb') as fh:
        byte_stream = fh.read()
    s3_key_prefix = cfg.get('s3_key_prefix', '/dist')
    checksum = hashlib.new('md5', byte_stream).hexdigest()
    timestamp = str(time.time())
    filename = '{prefix}{checksum}-{ts}.zip'.format(
        prefix=s3_key_prefix, checksum=checksum, ts=timestamp,
    )

    # Do we prefer development variable over config?
    buck_name = (
        os.environ.get('S3_BUCKET_NAME') or cfg.get('bucket_name')
    )
    func_name = (
        os.environ.get('LAMBDA_FUNCTION_NAME') or cfg.get('function_name')
    )
    kwargs = {
        'Bucket': '{}'.format(buck_name),
        'Key': '{}'.format(filename),
        'Body': byte_stream,
    }

    client.put_object(**kwargs)
    print('Finished uploading {} to S3 bucket {}'.format(func_name, buck_name))
    if use_s3:
        return filename