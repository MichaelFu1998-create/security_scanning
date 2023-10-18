def to_representation(self, instance):
        """
        Return the updated program data dictionary.

        Arguments:
            instance (dict): The program data.

        Returns:
            dict: The updated program data.
        """
        updated_program = copy.deepcopy(instance)
        enterprise_customer_catalog = self.context['enterprise_customer_catalog']
        updated_program['enrollment_url'] = enterprise_customer_catalog.get_program_enrollment_url(
            updated_program['uuid']
        )
        for course in updated_program['courses']:
            course['enrollment_url'] = enterprise_customer_catalog.get_course_enrollment_url(course['key'])
            for course_run in course['course_runs']:
                course_run['enrollment_url'] = enterprise_customer_catalog.get_course_run_enrollment_url(
                    course_run['key']
                )
        return updated_program