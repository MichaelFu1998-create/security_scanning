def application_exists(self):
        """
        Returns whether or not the given app_name exists
        """
        response = self.ebs.describe_applications(application_names=[self.app_name])
        return len(response['DescribeApplicationsResponse']['DescribeApplicationsResult']['Applications']) > 0