def get(self, request):
        """
        Render a form to collect user input about data sharing consent.
        """
        enterprise_customer_uuid = request.GET.get('enterprise_customer_uuid')
        success_url = request.GET.get('next')
        failure_url = request.GET.get('failure_url')
        course_id = request.GET.get('course_id', '')
        program_uuid = request.GET.get('program_uuid', '')
        self.preview_mode = bool(request.GET.get('preview_mode', False))

        # Get enterprise_customer to start in case we need to render a custom 404 page
        # Then go through other business logic to determine (and potentially overwrite) the enterprise customer
        enterprise_customer = get_enterprise_customer_or_404(enterprise_customer_uuid)
        context_data = get_global_context(request, enterprise_customer)

        if not self.preview_mode:
            if not self.course_or_program_exist(course_id, program_uuid):
                error_code = 'ENTGDS000'
                log_message = (
                    'Neither the course with course_id: {course_id} '
                    'or program with {program_uuid} exist for '
                    'enterprise customer {enterprise_customer_uuid}'
                    'Error code {error_code} presented to user {userid}'.format(
                        course_id=course_id,
                        program_uuid=program_uuid,
                        error_code=error_code,
                        userid=request.user.id,
                        enterprise_customer_uuid=enterprise_customer_uuid,
                    )
                )
                return render_page_with_error_code_message(request, context_data, error_code, log_message)

            try:
                consent_record = get_data_sharing_consent(
                    request.user.username,
                    enterprise_customer_uuid,
                    program_uuid=program_uuid,
                    course_id=course_id
                )
            except NotConnectedToOpenEdX as error:
                error_code = 'ENTGDS001'
                log_message = (
                    'The was a problem with getting the consent record of user {userid} with '
                    'uuid {enterprise_customer_uuid}. get_data_sharing_consent threw '
                    'the following NotConnectedToOpenEdX error: {error}'
                    'for course_id {course_id}.'
                    'Error code {error_code} presented to user'.format(
                        userid=request.user.id,
                        enterprise_customer_uuid=enterprise_customer_uuid,
                        error=error,
                        error_code=error_code,
                        course_id=course_id,
                    )
                )
                return render_page_with_error_code_message(request, context_data, error_code, log_message)

            try:
                consent_required = consent_record.consent_required()
            except AttributeError:
                consent_required = None

            if consent_record is None or not consent_required:
                error_code = 'ENTGDS002'
                log_message = (
                    'The was a problem with the consent record of user {userid} with '
                    'enterprise_customer_uuid {enterprise_customer_uuid}. consent_record has a value '
                    'of {consent_record} and consent_record.consent_required() a '
                    'value of {consent_required} for course_id {course_id}. '
                    'Error code {error_code} presented to user'.format(
                        userid=request.user.id,
                        enterprise_customer_uuid=enterprise_customer_uuid,
                        consent_record=consent_record,
                        consent_required=consent_required,
                        error_code=error_code,
                        course_id=course_id,
                    )
                )
                return render_page_with_error_code_message(request, context_data, error_code, log_message)
            else:
                enterprise_customer = consent_record.enterprise_customer
        elif not request.user.is_staff:
            raise PermissionDenied()

        # Retrieve context data again now that enterprise_customer logic has been run
        context_data = get_global_context(request, enterprise_customer)

        if not (enterprise_customer_uuid and success_url and failure_url):
            error_code = 'ENTGDS003'
            log_message = (
                'Error: one or more of the following values was falsy: '
                'enterprise_customer_uuid: {enterprise_customer_uuid}, '
                'success_url: {success_url}, '
                'failure_url: {failure_url} for course id {course_id}'
                'The following error code was reported to user {userid}: {error_code}'.format(
                    userid=request.user.id,
                    enterprise_customer_uuid=enterprise_customer_uuid,
                    success_url=success_url,
                    failure_url=failure_url,
                    error_code=error_code,
                    course_id=course_id,
                )
            )
            return render_page_with_error_code_message(request, context_data, error_code, log_message)

        try:
            updated_context_dict = self.get_course_or_program_context(
                enterprise_customer,
                course_id=course_id,
                program_uuid=program_uuid
            )
            context_data.update(updated_context_dict)
        except Http404:
            error_code = 'ENTGDS004'
            log_message = (
                'CourseCatalogApiServiceClient is improperly configured. '
                'Returned error code {error_code} to user {userid} '
                'and enterprise_customer {enterprise_customer} '
                'for course_id {course_id}'.format(
                    error_code=error_code,
                    userid=request.user.id,
                    enterprise_customer=enterprise_customer.uuid,
                    course_id=course_id,
                )
            )
            return render_page_with_error_code_message(request, context_data, error_code, log_message)

        item = 'course' if course_id else 'program'
        # Translators: bold_start and bold_end are HTML tags for specifying enterprise name in bold text.
        context_data.update({
            'consent_request_prompt': _(
                'To access this {item}, you must first consent to share your learning achievements '
                'with {bold_start}{enterprise_customer_name}{bold_end}.'
            ).format(
                enterprise_customer_name=enterprise_customer.name,
                bold_start='<b>',
                bold_end='</b>',
                item=item,
            ),
            'confirmation_alert_prompt': _(
                'In order to start this {item} and use your discount, {bold_start}you must{bold_end} consent '
                'to share your {item} data with {enterprise_customer_name}.'
            ).format(
                enterprise_customer_name=enterprise_customer.name,
                bold_start='<b>',
                bold_end='</b>',
                item=item,
            ),
            'redirect_url': success_url,
            'failure_url': failure_url,
            'defer_creation': request.GET.get('defer_creation') is not None,
            'requested_permissions': [
                _('your enrollment in this {item}').format(item=item),
                _('your learning progress'),
                _('course completion'),
            ],
            'policy_link_template': '',
        })
        platform_name = context_data['platform_name']
        published_only = False if self.preview_mode else True
        enterprise_consent_page = enterprise_customer.get_data_sharing_consent_text_overrides(
            published_only=published_only
        )
        if enterprise_consent_page:
            context_data.update(self.get_context_from_db(enterprise_consent_page, platform_name, item, context_data))
        else:
            context_data.update(self.get_default_context(enterprise_customer, platform_name))

        return render(request, 'enterprise/grant_data_sharing_permissions.html', context=context_data)