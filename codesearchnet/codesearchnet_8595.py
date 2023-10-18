def to_representation(self, instance):
        """
        Return the updated course data dictionary.

        Arguments:
            instance (dict): The course data.

        Returns:
            dict: The updated course data.
        """
        updated_course = copy.deepcopy(instance)
        enterprise_customer_catalog = self.context['enterprise_customer_catalog']
        updated_course['enrollment_url'] = enterprise_customer_catalog.get_course_enrollment_url(
            updated_course['key']
        )
        for course_run in updated_course['course_runs']:
            course_run['enrollment_url'] = enterprise_customer_catalog.get_course_run_enrollment_url(
                course_run['key']
            )
        return updated_course