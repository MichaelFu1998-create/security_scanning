def post(self, request, *args, **kwargs):
        """
        Run some custom POST logic for Enterprise workflows before routing the user through existing views.
        """
        # pylint: disable=unused-variable
        enterprise_customer_uuid, course_run_id, course_key, program_uuid = RouterView.get_path_variables(**kwargs)
        enterprise_customer = get_enterprise_customer_or_404(enterprise_customer_uuid)

        if course_key:
            context_data = get_global_context(request, enterprise_customer)
            try:
                kwargs['course_id'] = RouterView.get_course_run_id(request.user, enterprise_customer, course_key)
            except Http404:
                error_code = 'ENTRV001'
                log_message = (
                    'Could not find course run with id {course_run_id} '
                    'for course key {course_key} and '
                    'for enterprise_customer_uuid {enterprise_customer_uuid} '
                    'and program {program_uuid}. '
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

        return self.redirect(request, *args, **kwargs)