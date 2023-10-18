def download_s3(bucket_name, file_key, file_path, force=False):
    """Download a remote file from S3.
    """
    file_path = path(file_path)
    bucket = open_s3(bucket_name)

    file_dir = file_path.dirname()
    file_dir.makedirs()

    s3_key = bucket.get_key(file_key)
    if file_path.exists():
        file_data = file_path.bytes()
        file_md5, file_md5_64 = s3_key.get_md5_from_hexdigest(hashlib.md5(file_data).hexdigest())

        # Check the hash.
        try:
            s3_md5 = s3_key.etag.replace('"', '')
        except KeyError:
            pass
        else:
            if s3_md5 == file_md5:
                info('Hash is the same. Skipping %s' % file_path)
                return

            elif not force:
                # Check if file on S3 is older than local file.
                s3_datetime = datetime.datetime(*time.strptime(
                    s3_key.last_modified, '%a, %d %b %Y %H:%M:%S %Z')[0:6])
                local_datetime = datetime.datetime.utcfromtimestamp(file_path.stat().st_mtime)
                if s3_datetime < local_datetime:
                    info("File at %s is less recent than the local version." % (file_key))
                    return

    # If it is newer, let's process and upload
    info("Downloading %s..." % (file_key))

    try:
        with open(file_path, 'w') as fo:
            s3_key.get_contents_to_file(fo)
    except Exception as e:
        error("Failed: %s" % e)
        raise