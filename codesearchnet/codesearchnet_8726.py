def post(self, request, enterprise_uuid, course_id):
        """
        Process a submitted track selection form for the enterprise.
        """
        enterprise_customer, course, course_run, course_modes = self.get_base_details(
            request, enterprise_uuid, course_id
        )

        # Create a link between the user and the enterprise customer if it does not already exist.
        enterprise_customer_user, __ = EnterpriseCustomerUser.objects.get_or_create(
            enterprise_customer=enterprise_customer,
            user_id=request.user.id
        )
        enterprise_customer_user.update_session(request)

        data_sharing_consent = DataSharingConsent.objects.proxied_get(
            username=enterprise_customer_user.username,
            course_id=course_id,
            enterprise_customer=enterprise_customer
        )

        try:
            enterprise_course_enrollment = EnterpriseCourseEnrollment.objects.get(
                enterprise_customer_user__enterprise_customer=enterprise_customer,
                enterprise_customer_user__user_id=request.user.id,
                course_id=course_id
            )
        except EnterpriseCourseEnrollment.DoesNotExist:
            enterprise_course_enrollment = None

        enterprise_catalog_uuid = request.POST.get('catalog')
        selected_course_mode_name = request.POST.get('course_mode')
        cohort_name = request.POST.get('cohort')

        selected_course_mode = None
        for course_mode in course_modes:
            if course_mode['mode'] == selected_course_mode_name:
                selected_course_mode = course_mode
                break

        if not selected_course_mode:
            return self.get_enterprise_course_enrollment_page(
                request,
                enterprise_customer,
                course,
                course_run,
                course_modes,
                enterprise_course_enrollment,
                data_sharing_consent
            )

        user_consent_needed = get_data_sharing_consent(
            enterprise_customer_user.username,
            enterprise_customer.uuid,
            course_id=course_id
        ).consent_required()
        if not selected_course_mode.get('premium') and not user_consent_needed:
            # For the audit course modes (audit, honor), where DSC is not
            # required, enroll the learner directly through enrollment API
            # client and redirect the learner to LMS courseware page.
            if not enterprise_course_enrollment:
                # Create the Enterprise backend database records for this course enrollment.
                enterprise_course_enrollment = EnterpriseCourseEnrollment.objects.create(
                    enterprise_customer_user=enterprise_customer_user,
                    course_id=course_id,
                )
                track_enrollment('course-landing-page-enrollment', request.user.id, course_id, request.get_full_path())

            client = EnrollmentApiClient()
            client.enroll_user_in_course(
                request.user.username,
                course_id,
                selected_course_mode_name,
                cohort=cohort_name
            )

            return redirect(LMS_COURSEWARE_URL.format(course_id=course_id))

        if user_consent_needed:
            # For the audit course modes (audit, honor) or for the premium
            # course modes (Verified, Prof Ed) where DSC is required, redirect
            # the learner to course specific DSC with enterprise UUID from
            # there the learner will be directed to the ecommerce flow after
            # providing DSC.
            query_string_params = {
                'course_mode': selected_course_mode_name,
            }
            if enterprise_catalog_uuid:
                query_string_params.update({'catalog': enterprise_catalog_uuid})

            next_url = '{handle_consent_enrollment_url}?{query_string}'.format(
                handle_consent_enrollment_url=reverse(
                    'enterprise_handle_consent_enrollment', args=[enterprise_customer.uuid, course_id]
                ),
                query_string=urlencode(query_string_params)
            )

            failure_url = reverse('enterprise_course_run_enrollment_page', args=[enterprise_customer.uuid, course_id])
            if request.META['QUERY_STRING']:
                # Preserve all querystring parameters in the request to build
                # failure url, so that learner views the same enterprise course
                # enrollment page (after redirect) as for the first time.
                # Since this is a POST view so use `request.META` to get
                # querystring instead of `request.GET`.
                # https://docs.djangoproject.com/en/1.11/ref/request-response/#django.http.HttpRequest.META
                failure_url = '{course_enrollment_url}?{query_string}'.format(
                    course_enrollment_url=reverse(
                        'enterprise_course_run_enrollment_page', args=[enterprise_customer.uuid, course_id]
                    ),
                    query_string=request.META['QUERY_STRING']
                )

            return redirect(
                '{grant_data_sharing_url}?{params}'.format(
                    grant_data_sharing_url=reverse('grant_data_sharing_permissions'),
                    params=urlencode(
                        {
                            'next': next_url,
                            'failure_url': failure_url,
                            'enterprise_customer_uuid': enterprise_customer.uuid,
                            'course_id': course_id,
                        }
                    )
                )
            )

        # For the premium course modes (Verified, Prof Ed) where DSC is
        # not required, redirect the enterprise learner to the ecommerce
        # flow in LMS.
        # Note: LMS start flow automatically detects the paid mode
        premium_flow = LMS_START_PREMIUM_COURSE_FLOW_URL.format(course_id=course_id)
        if enterprise_catalog_uuid:
            premium_flow += '?catalog={catalog_uuid}'.format(
                catalog_uuid=enterprise_catalog_uuid
            )

        return redirect(premium_flow)