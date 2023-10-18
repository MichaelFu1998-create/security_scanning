def get(self, request, enterprise_uuid, course_id):
        """
        Show course track selection page for the enterprise.

        Based on `enterprise_uuid` in URL, the view will decide which
        enterprise customer's course enrollment page is to use.

        Unauthenticated learners will be redirected to enterprise-linked SSO.

        A 404 will be raised if any of the following conditions are met:
            * No enterprise customer uuid kwarg `enterprise_uuid` in request.
            * No enterprise customer found against the enterprise customer
                uuid `enterprise_uuid` in the request kwargs.
            * No course is found in database against the provided `course_id`.

        """
        # Check to see if access to the course run is restricted for this user.
        embargo_url = EmbargoApiClient.redirect_if_blocked([course_id], request.user, get_ip(request), request.path)
        if embargo_url:
            return redirect(embargo_url)

        enterprise_customer, course, course_run, modes = self.get_base_details(
            request, enterprise_uuid, course_id
        )
        enterprise_customer_user = get_enterprise_customer_user(request.user.id, enterprise_uuid)
        data_sharing_consent = DataSharingConsent.objects.proxied_get(
            username=enterprise_customer_user.username,
            course_id=course_id,
            enterprise_customer=enterprise_customer
        )

        enrollment_client = EnrollmentApiClient()
        enrolled_course = enrollment_client.get_course_enrollment(request.user.username, course_id)
        try:
            enterprise_course_enrollment = EnterpriseCourseEnrollment.objects.get(
                enterprise_customer_user__enterprise_customer=enterprise_customer,
                enterprise_customer_user__user_id=request.user.id,
                course_id=course_id
            )
        except EnterpriseCourseEnrollment.DoesNotExist:
            enterprise_course_enrollment = None

        if enrolled_course and enterprise_course_enrollment:
            # The user is already enrolled in the course through the Enterprise Customer, so redirect to the course
            # info page.
            return redirect(LMS_COURSEWARE_URL.format(course_id=course_id))

        return self.get_enterprise_course_enrollment_page(
            request,
            enterprise_customer,
            course,
            course_run,
            modes,
            enterprise_course_enrollment,
            data_sharing_consent,
        )