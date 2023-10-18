def update_course_runs(self, course_runs, enterprise_customer, enterprise_context):
        """
        Update Marketing urls in course metadata and return updated course.

        Arguments:
            course_runs (list): List of course runs.
            enterprise_customer (EnterpriseCustomer): enterprise customer instance.
            enterprise_context (dict): The context to inject into URLs.

        Returns:
            (dict): Dictionary containing updated course metadata.
        """
        updated_course_runs = []
        for course_run in course_runs:
            track_selection_url = utils.get_course_track_selection_url(
                course_run=course_run,
                query_parameters=dict(enterprise_context, **utils.get_enterprise_utm_context(enterprise_customer)),
            )

            enrollment_url = enterprise_customer.get_course_run_enrollment_url(course_run.get('key'))

            course_run.update({
                'enrollment_url': enrollment_url,
                'track_selection_url': track_selection_url,
            })

            # Update marketing urls in course metadata to include enterprise related info.
            marketing_url = course_run.get('marketing_url')
            if marketing_url:
                query_parameters = dict(enterprise_context, **utils.get_enterprise_utm_context(enterprise_customer))
                course_run.update({'marketing_url': utils.update_query_parameters(marketing_url, query_parameters)})

            # Add updated course run to the list.
            updated_course_runs.append(course_run)
        return updated_course_runs