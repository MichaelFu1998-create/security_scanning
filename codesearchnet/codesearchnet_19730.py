async def copy_storage_object(self, source_bucket, source_key,
                                  bucket, key):
        """Copy a file from one bucket into another
        """
        info = await self.head_object(Bucket=source_bucket, Key=source_key)
        size = info['ContentLength']

        if size > MULTI_PART_SIZE:
            result = await _multipart_copy(self, source_bucket, source_key,
                                           bucket, key, size)
        else:
            result = await self.copy_object(
                Bucket=bucket, Key=key,
                CopySource=_source_string(source_bucket, source_key)
            )
        return result