def get(self, request, enterprise_uuid, program_uuid):
        """
        Show Program Landing page for the Enterprise's Program.

        Render the Enterprise's Program Enrollment page for a specific program.
        The Enterprise and Program are both selected by their respective UUIDs.

        Unauthenticated learners will be redirected to enterprise-linked SSO.

        A 404 will be raised if any of the following conditions are met:
            * No enterprise customer UUID query parameter ``enterprise_uuid`` found in request.
            * No enterprise customer found against the enterprise customer
                uuid ``enterprise_uuid`` in the request kwargs.
            * No Program can be found given ``program_uuid`` either at all or associated with
                the Enterprise..
        """
        verify_edx_resources()

        enterprise_customer = get_enterprise_customer_or_404(enterprise_uuid)
        context_data = get_global_context(request, enterprise_customer)
        program_details, error_code = self.get_program_details(request, program_uuid, enterprise_customer)
        if error_code:
            return render(
                request,
                ENTERPRISE_GENERAL_ERROR_PAGE,
                context=context_data,
                status=404,
            )
        if program_details['certificate_eligible_for_program']:
            # The user is already enrolled in the program, so redirect to the program's dashboard.
            return redirect(LMS_PROGRAMS_DASHBOARD_URL.format(uuid=program_uuid))

        # Check to see if access to any of the course runs in the program are restricted for this user.
        course_run_ids = []
        for course in program_details['courses']:
            for course_run in course['course_runs']:
                course_run_ids.append(course_run['key'])
        embargo_url = EmbargoApiClient.redirect_if_blocked(course_run_ids, request.user, get_ip(request), request.path)
        if embargo_url:
            return redirect(embargo_url)

        return self.get_enterprise_program_enrollment_page(request, enterprise_customer, program_details)