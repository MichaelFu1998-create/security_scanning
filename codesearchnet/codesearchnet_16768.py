def get_environments(self):
        """
        Returns the environments
        """
        response = self.ebs.describe_environments(application_name=self.app_name, include_deleted=False)
        return response['DescribeEnvironmentsResponse']['DescribeEnvironmentsResult']['Environments']