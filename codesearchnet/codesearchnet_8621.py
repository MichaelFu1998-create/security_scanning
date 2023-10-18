def _collect_certificate_data(self, enterprise_enrollment):
        """
        Collect the learner completion data from the course certificate.

        Used for Instructor-paced courses.

        If no certificate is found, then returns the completed_date = None, grade = In Progress, on the idea that a
        certificate will eventually be generated.

        Args:
            enterprise_enrollment (EnterpriseCourseEnrollment): the enterprise enrollment record for which we need to
            collect completion/grade data

        Returns:
            completed_date: Date the course was completed, this is None if course has not been completed.
            grade: Current grade in the course.
            is_passing: Boolean indicating if the grade is a passing grade or not.
        """

        if self.certificates_api is None:
            self.certificates_api = CertificatesApiClient(self.user)

        course_id = enterprise_enrollment.course_id
        username = enterprise_enrollment.enterprise_customer_user.user.username

        try:
            certificate = self.certificates_api.get_course_certificate(course_id, username)
            completed_date = certificate.get('created_date')
            if completed_date:
                completed_date = parse_datetime(completed_date)
            else:
                completed_date = timezone.now()

            # For consistency with _collect_grades_data, we only care about Pass/Fail grades. This could change.
            is_passing = certificate.get('is_passing')
            grade = self.grade_passing if is_passing else self.grade_failing

        except HttpNotFoundError:
            completed_date = None
            grade = self.grade_incomplete
            is_passing = False

        return completed_date, grade, is_passing