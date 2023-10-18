def get(self, request, enterprise_uuid, course_id):
        """
        Handle the enrollment of enterprise learner in the provided course.

        Based on `enterprise_uuid` in URL, the view will decide which
        enterprise customer's course enrollment record should be created.

        Depending on the value of query parameter `course_mode` then learner
        will be either redirected to LMS dashboard for audit modes or
        redirected to ecommerce basket flow for payment of premium modes.
        """
        enrollment_course_mode = request.GET.get('course_mode')
        enterprise_catalog_uuid = request.GET.get('catalog')

        # Redirect the learner to LMS dashboard in case no course mode is
        # provided as query parameter `course_mode`
        if not enrollment_course_mode:
            return redirect(LMS_DASHBOARD_URL)

        enrollment_api_client = EnrollmentApiClient()
        course_modes = enrollment_api_client.get_course_modes(course_id)

        # Verify that the request user belongs to the enterprise against the
        # provided `enterprise_uuid`.
        enterprise_customer = get_enterprise_customer_or_404(enterprise_uuid)
        enterprise_customer_user = get_enterprise_customer_user(request.user.id, enterprise_customer.uuid)

        if not course_modes:
            context_data = get_global_context(request, enterprise_customer)
            error_code = 'ENTHCE000'
            log_message = (
                'No course_modes for course_id {course_id} for enterprise_catalog_uuid '
                '{enterprise_catalog_uuid}.'
                'The following error was presented to '
                'user {userid}: {error_code}'.format(
                    userid=request.user.id,
                    enterprise_catalog_uuid=enterprise_catalog_uuid,
                    course_id=course_id,
                    error_code=error_code
                )
            )
            return render_page_with_error_code_message(request, context_data, error_code, log_message)

        selected_course_mode = None
        for course_mode in course_modes:
            if course_mode['slug'] == enrollment_course_mode:
                selected_course_mode = course_mode
                break

        if not selected_course_mode:
            return redirect(LMS_DASHBOARD_URL)

        # Create the Enterprise backend database records for this course
        # enrollment
        __, created = EnterpriseCourseEnrollment.objects.get_or_create(
            enterprise_customer_user=enterprise_customer_user,
            course_id=course_id,
        )
        if created:
            track_enrollment('course-landing-page-enrollment', request.user.id, course_id, request.get_full_path())

        DataSharingConsent.objects.update_or_create(
            username=enterprise_customer_user.username,
            course_id=course_id,
            enterprise_customer=enterprise_customer_user.enterprise_customer,
            defaults={
                'granted': True
            },
        )

        audit_modes = getattr(settings, 'ENTERPRISE_COURSE_ENROLLMENT_AUDIT_MODES', ['audit', 'honor'])
        if selected_course_mode['slug'] in audit_modes:
            # In case of Audit course modes enroll the learner directly through
            # enrollment API client and redirect the learner to dashboard.
            enrollment_api_client.enroll_user_in_course(
                request.user.username, course_id, selected_course_mode['slug']
            )

            return redirect(LMS_COURSEWARE_URL.format(course_id=course_id))

        # redirect the enterprise learner to the ecommerce flow in LMS
        # Note: LMS start flow automatically detects the paid mode
        premium_flow = LMS_START_PREMIUM_COURSE_FLOW_URL.format(course_id=course_id)
        if enterprise_catalog_uuid:
            premium_flow += '?catalog={catalog_uuid}'.format(
                catalog_uuid=enterprise_catalog_uuid
            )

        return redirect(premium_flow)