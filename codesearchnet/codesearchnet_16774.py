def create_application_version(self, version_label, key):
        """
        Creates an application version
        """
        out("Creating application version " + str(version_label) + " for " + str(key))
        self.ebs.create_application_version(self.app_name, version_label,
                                            s3_bucket=self.aws.bucket, s3_key=self.aws.bucket_path+key)