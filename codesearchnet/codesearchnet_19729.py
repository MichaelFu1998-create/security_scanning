async def upload_file(self, bucket, file, uploadpath=None, key=None,
                          ContentType=None, **kw):
        """Upload a file to S3 possibly using the multi-part uploader
        Return the key uploaded
        """
        is_filename = False

        if hasattr(file, 'read'):
            if hasattr(file, 'seek'):
                file.seek(0)
            file = file.read()
            size = len(file)
        elif key:
            size = len(file)
        else:
            is_filename = True
            size = os.stat(file).st_size
            key = os.path.basename(file)

        assert key, 'key not available'

        if not ContentType:
            ContentType, _ = mimetypes.guess_type(key)

        if uploadpath:
            if not uploadpath.endswith('/'):
                uploadpath = '%s/' % uploadpath
            key = '%s%s' % (uploadpath, key)

        params = dict(Bucket=bucket, Key=key)

        if not ContentType:
            ContentType = 'application/octet-stream'

        params['ContentType'] = ContentType

        if size > MULTI_PART_SIZE and is_filename:
            resp = await _multipart(self, file, params)
        elif is_filename:
            with open(file, 'rb') as fp:
                params['Body'] = fp.read()
            resp = await self.put_object(**params)
        else:
            params['Body'] = file
            resp = await self.put_object(**params)
        if 'Key' not in resp:
            resp['Key'] = key
        if 'Bucket' not in resp:
            resp['Bucket'] = bucket
        return resp