def delete_course_references(course_key):
    """
    Inactivates references to course keys within this app (ref: receivers.py and api.py)
    """
    [_inactivate_record(record) for record in internal.OrganizationCourse.objects.filter(
        course_id=text_type(course_key),
        active=True
    )]