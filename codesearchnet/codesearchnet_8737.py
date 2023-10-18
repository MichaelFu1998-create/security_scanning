def get(self, request, *args, **kwargs):
        """
        Run some custom GET logic for Enterprise workflows before routing the user through existing views.

        In particular, before routing to existing views:
        - If the requested resource is a course, find the current course run for that course,
          and make that course run the requested resource instead.
        - Look to see whether a request is eligible for direct audit enrollment, and if so, directly enroll the user.
        """
        enterprise_customer_uuid, course_run_id, course_key, program_uuid = RouterView.get_path_variables(**kwargs)
        enterprise_customer = get_enterprise_customer_or_404(enterprise_customer_uuid)
        if course_key:
            try:
                course_run_id = RouterView.get_course_run_id(request.user, enterprise_customer, course_key)
            except Http404:
                context_data = get_global_context(request, enterprise_customer)
                error_code = 'ENTRV000'
                log_message = (
                    'Could not find course run with id {course_run_id} '
                    'for course key {course_key} and program_uuid {program_uuid} '
                    'for enterprise_customer_uuid {enterprise_customer_uuid} '
                    'Returned error code {error_code} to user {userid}'.format(
                        course_key=course_key,
                        course_run_id=course_run_id,
                        enterprise_customer_uuid=enterprise_customer_uuid,
                        error_code=error_code,
                        userid=request.user.id,
                        program_uuid=program_uuid,
                    )
                )
                return render_page_with_error_code_message(request, context_data, error_code, log_message)
            kwargs['course_id'] = course_run_id

        # Ensure that the link is saved to the database prior to making some call in a downstream view
        # which may need to know that the user belongs to an enterprise customer.
        with transaction.atomic():
            enterprise_customer_user, __ = EnterpriseCustomerUser.objects.get_or_create(
                enterprise_customer=enterprise_customer,
                user_id=request.user.id
            )
            enterprise_customer_user.update_session(request)

        # Directly enroll in audit mode if the request in question has full direct audit enrollment eligibility.
        resource_id = course_run_id or program_uuid
        if self.eligible_for_direct_audit_enrollment(request, enterprise_customer, resource_id, course_key):
            try:
                enterprise_customer_user.enroll(resource_id, 'audit', cohort=request.GET.get('cohort', None))
                track_enrollment('direct-audit-enrollment', request.user.id, resource_id, request.get_full_path())
            except (CourseEnrollmentDowngradeError, CourseEnrollmentPermissionError):
                pass
            # The courseware view logic will check for DSC requirements, and route to the DSC page if necessary.
            return redirect(LMS_COURSEWARE_URL.format(course_id=resource_id))

        return self.redirect(request, *args, **kwargs)