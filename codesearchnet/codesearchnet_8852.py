def parse_course_key(course_identifier):
    """
    Return the serialized course key given either a course run ID or course key.
    """
    try:
        course_run_key = CourseKey.from_string(course_identifier)
    except InvalidKeyError:
        # Assume we already have a course key.
        return course_identifier

    return quote_plus(' '.join([course_run_key.org, course_run_key.course]))