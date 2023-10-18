def _collect_grades_data(self, enterprise_enrollment, course_details):
        """
        Collect the learner completion data from the Grades API.

        Used for self-paced courses.

        Args:
            enterprise_enrollment (EnterpriseCourseEnrollment): the enterprise enrollment record for which we need to
            collect completion/grade data
            course_details (dict): the course details for the course in the enterprise enrollment record.

        Returns:
            completed_date: Date the course was completed, this is None if course has not been completed.
            grade: Current grade in the course.
            is_passing: Boolean indicating if the grade is a passing grade or not.
        """
        if self.grades_api is None:
            self.grades_api = GradesApiClient(self.user)

        course_id = enterprise_enrollment.course_id
        username = enterprise_enrollment.enterprise_customer_user.user.username

        try:
            grades_data = self.grades_api.get_course_grade(course_id, username)

        except HttpNotFoundError as error:
            # Grade not found, so we have nothing to report.
            if hasattr(error, 'content'):
                response_content = json.loads(error.content)
                if response_content.get('error_code', '') == 'user_not_enrolled':
                    # This means the user has an enterprise enrollment record but is not enrolled in the course yet
                    LOGGER.info(
                        "User [%s] not enrolled in course [%s], enterprise enrollment [%d]",
                        username,
                        course_id,
                        enterprise_enrollment.pk
                    )
                    return None, None, None

            LOGGER.error("No grades data found for [%d]: [%s], [%s]", enterprise_enrollment.pk, course_id, username)
            return None, None, None

        # Prepare to process the course end date and pass/fail grade
        course_end_date = course_details.get('end')
        if course_end_date is not None:
            course_end_date = parse_datetime(course_end_date)
        now = timezone.now()
        is_passing = grades_data.get('passed')

        # We can consider a course complete if:
        # * the course's end date has passed
        if course_end_date is not None and course_end_date < now:
            completed_date = course_end_date
            grade = self.grade_passing if is_passing else self.grade_failing

        # * Or, the learner has a passing grade (as of now)
        elif is_passing:
            completed_date = now
            grade = self.grade_passing

        # Otherwise, the course is still in progress
        else:
            completed_date = None
            grade = self.grade_incomplete

        return completed_date, grade, is_passing