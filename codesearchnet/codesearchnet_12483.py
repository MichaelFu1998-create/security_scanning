def upload(self, local_file, s3_path=None):
        '''
        Upload files to your DG S3 bucket/prefix.

        Args:
            local_file (str): a path to a local file to upload, directory structures are not mirrored
            s3_path: a key (location) on s3 to upload the file to

        Returns:
            str: s3 path file was saved to

        Examples:
            >>> upload('path/to/image.tif')
            'mybucket/myprefix/image.tif'

            >>> upload('./images/image.tif')
            'mybucket/myprefix/image.tif'

            >>> upload('./images/image.tif', s3_path='images/image.tif')
            'mybucket/myprefix/images/image.tif'
        '''
        if not os.path.exists(local_file):
            raise Exception(local_file + " does not exist.")
            
        if s3_path is None:
            s3_path = os.path.basename(local_file)

        bucket = self.info['bucket']
        prefix = self.info['prefix']

        self.logger.debug('Connecting to S3')
        s3conn = self.client 
        self.logger.debug('Uploading file {}'.format(local_file))
        s3conn.upload_file(local_file, bucket, prefix+'/'+s3_path)
        self.logger.debug('Done!')
        return '{}/{}/{}'.format(bucket, prefix, s3_path)