def get_or_create_bucket(self, name):
        """
        Gets an S3 bucket of the given name, creating one if it doesn't already exist.

        Should be called with a role, if AWS credentials are stored in role settings. e.g.

            fab local s3.get_or_create_bucket:mybucket
        """
        from boto.s3 import connection
        if self.dryrun:
            print('boto.connect_s3().create_bucket(%s)' % repr(name))
        else:
            conn = connection.S3Connection(
                self.genv.aws_access_key_id,
                self.genv.aws_secret_access_key
            )
            bucket = conn.create_bucket(name)
            return bucket