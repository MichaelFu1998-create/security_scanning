def course_modal(context, course=None):
    """
    Django template tag that returns course information to display in a modal.

    You may pass in a particular course if you like. Otherwise, the modal will look for course context
    within the parent context.

    Usage:
        {% course_modal %}
        {% course_modal course %}
    """
    if course:
        context.update({
            'course_image_uri': course.get('course_image_uri', ''),
            'course_title': course.get('course_title', ''),
            'course_level_type': course.get('course_level_type', ''),
            'course_short_description': course.get('course_short_description', ''),
            'course_effort': course.get('course_effort', ''),
            'course_full_description': course.get('course_full_description', ''),
            'expected_learning_items': course.get('expected_learning_items', []),
            'staff': course.get('staff', []),
            'premium_modes': course.get('premium_modes', []),
        })
    return context