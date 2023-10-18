async def _upload_file(self, full_path):
        """Coroutine for uploading a single file
        """
        rel_path = os.path.relpath(full_path, self.folder)
        key = s3_key(os.path.join(self.key, rel_path))
        ct = self.content_types.get(key.split('.')[-1])
        with open(full_path, 'rb') as fp:
            file = fp.read()
        try:
            await self.botocore.upload_file(self.bucket, file, key=key,
                                            ContentType=ct)
        except Exception as exc:
            LOGGER.error('Could not upload "%s": %s', key, exc)
            self.failures[key] = self.all.pop(full_path)
            return
        size = self.all.pop(full_path)
        self.success[key] = size
        self.total_size += size
        percentage = 100*(1 - len(self.all)/self.total_files)
        message = '{0:.0f}% completed - uploaded "{1}" - {2}'.format(
            percentage, key, convert_bytes(size))
        LOGGER.info(message)