def post(self, request):
        """
        Process the above form.
        """
        enterprise_uuid = request.POST.get('enterprise_customer_uuid')
        success_url = request.POST.get('redirect_url')
        failure_url = request.POST.get('failure_url')
        course_id = request.POST.get('course_id', '')
        program_uuid = request.POST.get('program_uuid', '')

        enterprise_customer = get_enterprise_customer_or_404(enterprise_uuid)
        context_data = get_global_context(request, enterprise_customer)

        if not (enterprise_uuid and success_url and failure_url):
            error_code = 'ENTGDS005'
            log_message = (
                'Error: one or more of the following values was falsy: '
                'enterprise_uuid: {enterprise_uuid}, '
                'success_url: {success_url}, '
                'failure_url: {failure_url} for course_id {course_id}. '
                'The following error code was reported to the user {userid}: {error_code}'.format(
                    userid=request.user.id,
                    enterprise_uuid=enterprise_uuid,
                    success_url=success_url,
                    failure_url=failure_url,
                    error_code=error_code,
                    course_id=course_id,
                )
            )
            return render_page_with_error_code_message(request, context_data, error_code, log_message)

        if not self.course_or_program_exist(course_id, program_uuid):
            error_code = 'ENTGDS006'
            log_message = (
                'Neither the course with course_id: {course_id} '
                'or program with {program_uuid} exist for '
                'enterprise customer {enterprise_uuid}'
                'Error code {error_code} presented to user {userid}'.format(
                    course_id=course_id,
                    program_uuid=program_uuid,
                    error_code=error_code,
                    userid=request.user.id,
                    enterprise_uuid=enterprise_uuid,
                )
            )
            return render_page_with_error_code_message(request, context_data, error_code, log_message)

        consent_record = get_data_sharing_consent(
            request.user.username,
            enterprise_uuid,
            program_uuid=program_uuid,
            course_id=course_id
        )
        if consent_record is None:
            error_code = 'ENTGDS007'
            log_message = (
                'The was a problem with the consent record of user {userid} with '
                'enterprise_uuid {enterprise_uuid}. consent_record has a value '
                'of {consent_record} and a '
                'value for course_id {course_id}. '
                'Error code {error_code} presented to user'.format(
                    userid=request.user.id,
                    enterprise_uuid=enterprise_uuid,
                    consent_record=consent_record,
                    error_code=error_code,
                    course_id=course_id,
                )
            )
            return render_page_with_error_code_message(request, context_data, error_code, log_message)

        defer_creation = request.POST.get('defer_creation')
        consent_provided = bool(request.POST.get('data_sharing_consent', False))
        if defer_creation is None and consent_record.consent_required():
            if course_id:
                enterprise_customer_user, __ = EnterpriseCustomerUser.objects.get_or_create(
                    enterprise_customer=consent_record.enterprise_customer,
                    user_id=request.user.id
                )
                enterprise_customer_user.update_session(request)
                __, created = EnterpriseCourseEnrollment.objects.get_or_create(
                    enterprise_customer_user=enterprise_customer_user,
                    course_id=course_id,
                )
                if created:
                    track_enrollment('data-consent-page-enrollment', request.user.id, course_id, request.path)

            consent_record.granted = consent_provided
            consent_record.save()

        return redirect(success_url if consent_provided else failure_url)