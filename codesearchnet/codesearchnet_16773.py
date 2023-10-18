def get_versions(self):
        """
        Returns the versions available
        """
        response = self.ebs.describe_application_versions(application_name=self.app_name)
        return response['DescribeApplicationVersionsResponse']['DescribeApplicationVersionsResult']['ApplicationVersions']