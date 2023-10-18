def course_key_is_valid(course_key):
    """
    Course key object validation
    """
    if course_key is None:
        return False
    try:
        CourseKey.from_string(text_type(course_key))
    except (InvalidKeyError, UnicodeDecodeError):
        return False
    return True