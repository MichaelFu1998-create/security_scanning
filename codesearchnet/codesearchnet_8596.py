def to_representation(self, instance):
        """
        Return the updated course run data dictionary.

        Arguments:
            instance (dict): The course run data.

        Returns:
            dict: The updated course run data.
        """
        updated_course_run = copy.deepcopy(instance)
        enterprise_customer_catalog = self.context['enterprise_customer_catalog']
        updated_course_run['enrollment_url'] = enterprise_customer_catalog.get_course_run_enrollment_url(
            updated_course_run['key']
        )
        return updated_course_run