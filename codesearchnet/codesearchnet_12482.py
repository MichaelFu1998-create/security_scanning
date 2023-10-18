def delete(self, location):
        '''Delete content in bucket/prefix/location.
           Location can be a directory or a file (e.g., my_dir or my_dir/my_image.tif)
           If location is a directory, all files in the directory are deleted.
           If it is a file, then that file is deleted.

           Args:
               location (str): S3 location within prefix. Can be a directory or
                               a file (e.g., my_dir or my_dir/my_image.tif).
        '''
        bucket = self.info['bucket']
        prefix = self.info['prefix']

        self.logger.debug('Connecting to S3')
        s3conn = self.client 

        # remove head and/or trail backslash from location
        if location[0] == '/':
            location = location[1:]
        if location[-1] == '/':
            location = location[:-2]

        self.logger.debug('Deleting contents')

        for s3key in s3conn.list_objects(Bucket=bucket, Prefix=(prefix+'/'+location))['Contents']:
            s3conn.delete_object(Bucket=bucket, Key=s3key['Key'])

        self.logger.debug('Done!')