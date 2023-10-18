def upload_archive(self, filename, key, auto_create_bucket=True):
        """
        Uploads an application archive version to s3
        """
        try:
            bucket = self.s3.get_bucket(self.aws.bucket)
            if ((
                  self.aws.region != 'us-east-1' and self.aws.region != 'eu-west-1') and bucket.get_location() != self.aws.region) or (
                  self.aws.region == 'us-east-1' and bucket.get_location() != '') or (
                  self.aws.region == 'eu-west-1' and bucket.get_location() != 'eu-west-1'):
                raise Exception("Existing bucket doesn't match region")
        except S3ResponseError:
            bucket = self.s3.create_bucket(self.aws.bucket, location=self.aws.region)

        def __report_upload_progress(sent, total):
            if not sent:
                sent = 0
            if not total:
                total = 0
            out("Uploaded " + str(sent) + " bytes of " + str(total) \
                + " (" + str(int(float(max(1, sent)) / float(total) * 100)) + "%)")

        # upload the new version
        k = Key(bucket)
        k.key = self.aws.bucket_path + key
        k.set_metadata('time', str(time()))
        k.set_contents_from_filename(filename, cb=__report_upload_progress, num_cb=10)