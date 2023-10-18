def _validate_course_key(course_key):
    """ Validation helper """
    if not validators.course_key_is_valid(course_key):
        exceptions.raise_exception(
            "CourseKey",
            course_key,
            exceptions.InvalidCourseKeyException
        )