def eligible_for_direct_audit_enrollment(self, request, enterprise_customer, resource_id, course_key=None):
        """
        Return whether a request is eligible for direct audit enrollment for a particular enterprise customer.

        'resource_id' can be either course_run_id or program_uuid.
        We check for the following criteria:
        - The `audit` query parameter.
        - The user's being routed to the course enrollment landing page.
        - The customer's catalog contains the course in question.
        - The audit track is an available mode for the course.
        """
        course_identifier = course_key if course_key else resource_id

        # Return it in one big statement to utilize short-circuiting behavior. Avoid the API call if possible.
        return request.GET.get('audit') and \
            request.path == self.COURSE_ENROLLMENT_VIEW_URL.format(enterprise_customer.uuid, course_identifier) and \
            enterprise_customer.catalog_contains_course(resource_id) and \
            EnrollmentApiClient().has_course_mode(resource_id, 'audit')