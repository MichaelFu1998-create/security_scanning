def clean_course(self):
        """
        Verify course ID and retrieve course details.
        """
        course_id = self.cleaned_data[self.Fields.COURSE].strip()
        if not course_id:
            return None
        try:
            client = EnrollmentApiClient()
            return client.get_course_details(course_id)
        except (HttpClientError, HttpServerError):
            raise ValidationError(ValidationMessages.INVALID_COURSE_ID.format(course_id=course_id))