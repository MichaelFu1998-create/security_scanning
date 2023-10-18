def describe_events(self, environment_name, next_token=None, start_time=None):
        """
        Describes events from the given environment
        """
        events = self.ebs.describe_events(
            application_name=self.app_name,
            environment_name=environment_name,
            next_token=next_token,
            start_time=start_time + 'Z')

        return (events['DescribeEventsResponse']['DescribeEventsResult']['Events'], events['DescribeEventsResponse']['DescribeEventsResult']['NextToken'])