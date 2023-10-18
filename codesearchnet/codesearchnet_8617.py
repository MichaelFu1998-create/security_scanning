def update_course(self, course, enterprise_customer, enterprise_context):
        """
        Update course metadata of the given course and return updated course.

        Arguments:
            course (dict): Course Metadata returned by course catalog API
            enterprise_customer (EnterpriseCustomer): enterprise customer instance.
            enterprise_context (dict): Enterprise context to be added to course runs and URLs..

        Returns:
            (dict): Updated course metadata
        """
        course['course_runs'] = self.update_course_runs(
            course_runs=course.get('course_runs') or [],
            enterprise_customer=enterprise_customer,
            enterprise_context=enterprise_context,
        )

        # Update marketing urls in course metadata to include enterprise related info (i.e. our global context).
        marketing_url = course.get('marketing_url')
        if marketing_url:
            query_parameters = dict(enterprise_context, **utils.get_enterprise_utm_context(enterprise_customer))
            course.update({'marketing_url': utils.update_query_parameters(marketing_url, query_parameters)})

        # Finally, add context to the course as a whole.
        course.update(enterprise_context)
        return course