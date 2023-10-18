def get_active_course_runs(course, users_all_enrolled_courses):
    """
    Return active course runs (user is enrolled in) of the given course.

    This function will return the course_runs of 'course' which have
    active enrollment by looking into 'users_all_enrolled_courses'
    """
    # User's all course_run ids in which he has enrolled.
    enrolled_course_run_ids = [
        enrolled_course_run['course_details']['course_id'] for enrolled_course_run in users_all_enrolled_courses
        if enrolled_course_run['is_active'] and enrolled_course_run.get('course_details')
    ]
    return [course_run for course_run in course['course_runs'] if course_run['key'] in enrolled_course_run_ids]