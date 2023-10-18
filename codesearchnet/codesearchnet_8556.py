def get_course_certificate(self, course_id, username):
        """
        Retrieve the certificate for the given username for the given course_id.

        Args:
        * ``course_id`` (str): The string value of the course's unique identifier
        * ``username`` (str): The username ID identifying the user for which to retrieve the certificate

        Raises:

        HttpNotFoundError if no certificate found for the given user+course.

        Returns:

        a dict containing:

        * ``username``: A string representation of an user's username passed in the request.
        * ``course_id``: A string representation of a Course ID.
        * ``certificate_type``: A string representation of the certificate type.
        * ``created_date`: Datetime the certificate was created (tz-aware).
        * ``status``: A string representation of the certificate status.
        * ``is_passing``: True if the certificate has a passing status, False if not.
        * ``download_url``: A string representation of the certificate url.
        * ``grade``: A string representation of a float for the user's course grade.

        """
        return self.client.certificates(username).courses(course_id).get()