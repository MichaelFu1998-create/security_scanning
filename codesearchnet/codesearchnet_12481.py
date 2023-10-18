def download(self, location, local_dir='.'):
        '''Download content from bucket/prefix/location.
           Location can be a directory or a file (e.g., my_dir or my_dir/my_image.tif)
           If location is a directory, all files in the directory are
           downloaded. If it is a file, then that file is downloaded.

           Args:
               location (str): S3 location within prefix.
               local_dir (str): Local directory where file(s) will be stored.
                                Default is here.
        '''

        self.logger.debug('Getting S3 info')
        bucket = self.info['bucket']
        prefix = self.info['prefix']

        self.logger.debug('Connecting to S3')
        s3conn = self.client

        # remove head and/or trail backslash from location
        location = location.strip('/')

        self.logger.debug('Downloading contents')
        objects = s3conn.list_objects(Bucket=bucket, Prefix=(prefix+'/'+location))
        if 'Contents' not in objects:
            raise ValueError('Download target {}/{}/{} was not found or inaccessible.'.format(bucket, prefix, location))
        for s3key in objects['Contents']:
            key = s3key['Key']
    
            # skip directory keys
            if not key or key.endswith('/'):
                continue

            # get path to each file
            filepath = key.replace(prefix+'/'+location, '', 1).lstrip('/')
            filename = key.split('/')[-1]
            
            #self.logger.debug(filename)
            file_dir = filepath.split('/')[:-1]
            file_dir = '/'.join(file_dir)
            full_dir = os.path.join(local_dir, file_dir)

            # make sure directory exists
            if not os.path.isdir(full_dir):
                os.makedirs(full_dir)

            # download file
            s3conn.download_file(bucket, key, os.path.join(full_dir, filename))

        self.logger.debug('Done!')