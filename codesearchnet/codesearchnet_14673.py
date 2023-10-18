def init(self):
        """Create a bucket.
        """
        try:
            self.client.create_bucket(
                Bucket=self.db_path,
                CreateBucketConfiguration=self.bucket_configuration)
        except botocore.exceptions.ClientError as e:
            # If the bucket already exists
            if 'BucketAlreadyOwnedByYou' not in str(
                    e.response['Error']['Code']):
                raise e