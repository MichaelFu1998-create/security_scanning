def enroll_users_in_course(cls, enterprise_customer, course_id, course_mode, emails):
        """
        Enroll existing users in a course, and create a pending enrollment for nonexisting users.

        Args:
            enterprise_customer: The EnterpriseCustomer which is sponsoring the enrollment
            course_id (str): The unique identifier of the course in which we're enrolling
            course_mode (str): The mode with which we're enrolling in the course
            emails: An iterable of email addresses which need to be enrolled

        Returns:
            successes: A list of users who were successfully enrolled in the course
            pending: A list of PendingEnterpriseCustomerUsers who were successfully linked and had
                pending enrollments created for them in the database
            failures: A list of users who could not be enrolled in the course
        """
        existing_users, unregistered_emails = cls.get_users_by_email(emails)

        successes = []
        pending = []
        failures = []

        for user in existing_users:
            succeeded = cls.enroll_user(enterprise_customer, user, course_mode, course_id)
            if succeeded:
                successes.append(user)
            else:
                failures.append(user)

        for email in unregistered_emails:
            pending_user = enterprise_customer.enroll_user_pending_registration(
                email,
                course_mode,
                course_id
            )
            pending.append(pending_user)

        return successes, pending, failures