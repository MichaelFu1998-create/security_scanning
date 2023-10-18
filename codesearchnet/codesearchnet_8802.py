def enroll_user(cls, enterprise_customer, user, course_mode, *course_ids):
        """
        Enroll a single user in any number of courses using a particular course mode.

        Args:
            enterprise_customer: The EnterpriseCustomer which is sponsoring the enrollment
            user: The user who needs to be enrolled in the course
            course_mode: The mode with which the enrollment should be created
            *course_ids: An iterable containing any number of course IDs to eventually enroll the user in.

        Returns:
            Boolean: Whether or not enrollment succeeded for all courses specified
        """
        enterprise_customer_user, __ = EnterpriseCustomerUser.objects.get_or_create(
            enterprise_customer=enterprise_customer,
            user_id=user.id
        )
        enrollment_client = EnrollmentApiClient()
        succeeded = True
        for course_id in course_ids:
            try:
                enrollment_client.enroll_user_in_course(user.username, course_id, course_mode)
            except HttpClientError as exc:
                # Check if user is already enrolled then we should ignore exception
                if cls.is_user_enrolled(user, course_id, course_mode):
                    succeeded = True
                else:
                    succeeded = False
                    default_message = 'No error message provided'
                    try:
                        error_message = json.loads(exc.content.decode()).get('message', default_message)
                    except ValueError:
                        error_message = default_message
                    logging.error(
                        'Error while enrolling user %(user)s: %(message)s',
                        dict(user=user.username, message=error_message)
                    )
            if succeeded:
                __, created = EnterpriseCourseEnrollment.objects.get_or_create(
                    enterprise_customer_user=enterprise_customer_user,
                    course_id=course_id
                )
                if created:
                    track_enrollment('admin-enrollment', user.id, course_id)
        return succeeded