def transform_launch_points(self, content_metadata_item):
        """
        Return the content metadata item launch points.

        SAPSF allows you to transmit an arry of content launch points which
        are meant to represent sections of a content item which a learner can
        launch into from SAPSF. Currently, we only provide a single launch
        point for a content item.
        """
        return [{
            'providerID': self.enterprise_configuration.provider_id,
            'launchURL': content_metadata_item['enrollment_url'],
            'contentTitle': content_metadata_item['title'],
            'contentID': self.get_content_id(content_metadata_item),
            'launchType': 3,  # This tells SAPSF to launch the course in a new browser window.
            'mobileEnabled': True,  # Always return True per ENT-1401
            'mobileLaunchURL': content_metadata_item['enrollment_url'],
        }]