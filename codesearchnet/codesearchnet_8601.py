def create(self, validated_data):
        """
        Perform the enrollment for existing enterprise customer users, or create the pending objects for new users.
        """
        enterprise_customer = self.context.get('enterprise_customer')
        lms_user = validated_data.get('lms_user_id')
        tpa_user = validated_data.get('tpa_user_id')
        user_email = validated_data.get('user_email')
        course_run_id = validated_data.get('course_run_id')
        course_mode = validated_data.get('course_mode')
        cohort = validated_data.get('cohort')
        email_students = validated_data.get('email_students')
        is_active = validated_data.get('is_active')

        enterprise_customer_user = lms_user or tpa_user or user_email

        if isinstance(enterprise_customer_user, models.EnterpriseCustomerUser):
            validated_data['enterprise_customer_user'] = enterprise_customer_user
            try:
                if is_active:
                    enterprise_customer_user.enroll(course_run_id, course_mode, cohort=cohort)
                else:
                    enterprise_customer_user.unenroll(course_run_id)
            except (CourseEnrollmentDowngradeError, CourseEnrollmentPermissionError, HttpClientError) as exc:
                validated_data['detail'] = str(exc)
                return validated_data

            if is_active:
                track_enrollment('enterprise-customer-enrollment-api', enterprise_customer_user.user_id, course_run_id)
        else:
            if is_active:
                enterprise_customer_user = enterprise_customer.enroll_user_pending_registration(
                    user_email,
                    course_mode,
                    course_run_id,
                    cohort=cohort
                )
            else:
                enterprise_customer.clear_pending_registration(user_email, course_run_id)

        if email_students:
            enterprise_customer.notify_enrolled_learners(
                self.context.get('request_user'),
                course_run_id,
                [enterprise_customer_user]
            )

        validated_data['detail'] = 'success'

        return validated_data