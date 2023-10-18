def _validate_course(self):
        """
        Verify that the selected mode is valid for the given course .
        """
        # Verify that the selected mode is valid for the given course .
        course_details = self.cleaned_data.get(self.Fields.COURSE)
        if course_details:
            course_mode = self.cleaned_data.get(self.Fields.COURSE_MODE)
            if not course_mode:
                raise ValidationError(ValidationMessages.COURSE_WITHOUT_COURSE_MODE)
            valid_course_modes = course_details["course_modes"]
            if all(course_mode != mode["slug"] for mode in valid_course_modes):
                error = ValidationError(ValidationMessages.COURSE_MODE_INVALID_FOR_COURSE.format(
                    course_mode=course_mode,
                    course_id=course_details["course_id"],
                ))
                raise ValidationError({self.Fields.COURSE_MODE: error})