def environment_exists(self, env_name):
        """
        Returns whether or not the given environment exists
        """
        response = self.ebs.describe_environments(application_name=self.app_name, environment_names=[env_name],
                                                  include_deleted=False)
        return len(response['DescribeEnvironmentsResponse']['DescribeEnvironmentsResult']['Environments']) > 0 \
               and response['DescribeEnvironmentsResponse']['DescribeEnvironmentsResult']['Environments'][0][
                       'Status'] != 'Terminated'