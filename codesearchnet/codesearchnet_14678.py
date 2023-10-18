def is_initialized(self):
        """Check if bucket exists.
        :return: True if initialized, False otherwise
        """
        try:
            return self.client.head_bucket(
                Bucket=self.db_path)['ResponseMetadata']['HTTPStatusCode'] \
                   == 200
        except botocore.exceptions.ClientError as e:
            # If a client error is thrown, then check that it was a 404 error.
            # If it was a 404 error, then the bucket does not exist.
            if 'NoSuchBucket' in str(e.response['Error']['Code']):
                return False
            raise e