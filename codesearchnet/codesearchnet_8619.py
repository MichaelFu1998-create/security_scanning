def export(self):
        """
        Collect learner data for the ``EnterpriseCustomer`` where data sharing consent is granted.

        Yields a learner data object for each enrollment, containing:

        * ``enterprise_enrollment``: ``EnterpriseCourseEnrollment`` object.
        * ``completed_date``: datetime instance containing the course/enrollment completion date; None if not complete.
          "Course completion" occurs for instructor-paced courses when course certificates are issued, and
          for self-paced courses, when the course end date is passed, or when the learner achieves a passing grade.
        * ``grade``: string grade recorded for the learner in the course.
        """
        # Fetch the consenting enrollment data, including the enterprise_customer_user.
        # Order by the course_id, to avoid fetching course API data more than we have to.
        enrollment_queryset = EnterpriseCourseEnrollment.objects.select_related(
            'enterprise_customer_user'
        ).filter(
            enterprise_customer_user__enterprise_customer=self.enterprise_customer,
            enterprise_customer_user__active=True,
        ).order_by('course_id')

        # Fetch course details from the Course API, and cache between calls.
        course_details = None
        for enterprise_enrollment in enrollment_queryset:

            course_id = enterprise_enrollment.course_id

            # Fetch course details from Courses API
            # pylint: disable=unsubscriptable-object
            if course_details is None or course_details['course_id'] != course_id:
                if self.course_api is None:
                    self.course_api = CourseApiClient()
                course_details = self.course_api.get_course_details(course_id)

            if course_details is None:
                # Course not found, so we have nothing to report.
                LOGGER.error("No course run details found for enrollment [%d]: [%s]",
                             enterprise_enrollment.pk, course_id)
                continue

            consent = DataSharingConsent.objects.proxied_get(
                username=enterprise_enrollment.enterprise_customer_user.username,
                course_id=enterprise_enrollment.course_id,
                enterprise_customer=enterprise_enrollment.enterprise_customer_user.enterprise_customer
            )

            if not consent.granted or enterprise_enrollment.audit_reporting_disabled:
                continue

            # For instructor-paced courses, let the certificate determine course completion
            if course_details.get('pacing') == 'instructor':
                completed_date, grade, is_passing = self._collect_certificate_data(enterprise_enrollment)

            # For self-paced courses, check the Grades API
            else:
                completed_date, grade, is_passing = self._collect_grades_data(enterprise_enrollment, course_details)

            records = self.get_learner_data_records(
                enterprise_enrollment=enterprise_enrollment,
                completed_date=completed_date,
                grade=grade,
                is_passing=is_passing,
            )
            if records:
                # There are some cases where we won't receive a record from the above
                # method; right now, that should only happen if we have an Enterprise-linked
                # user for the integrated channel, and transmission of that user's
                # data requires an upstream user identifier that we don't have (due to a
                # failure of SSO or similar). In such a case, `get_learner_data_record`
                # would return None, and we'd simply skip yielding it here.
                for record in records:
                    yield record