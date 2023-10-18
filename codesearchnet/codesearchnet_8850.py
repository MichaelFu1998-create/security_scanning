def get_current_course_run(course, users_active_course_runs):
    """
    Return the current course run on the following conditions.

    - If user has active course runs (already enrolled) then return course run with closest start date
    Otherwise it will check the following logic:
    - Course run is enrollable (see is_course_run_enrollable)
    - Course run has a verified seat and the upgrade deadline has not expired.
    - Course run start date is closer to now than any other enrollable/upgradeable course runs.
    - If no enrollable/upgradeable course runs, return course run with most recent start date.
    """
    current_course_run = None
    filtered_course_runs = []
    all_course_runs = course['course_runs']

    if users_active_course_runs:
        current_course_run = get_closest_course_run(users_active_course_runs)
    else:
        for course_run in all_course_runs:
            if is_course_run_enrollable(course_run) and is_course_run_upgradeable(course_run):
                filtered_course_runs.append(course_run)

        if not filtered_course_runs:
            # Consider all runs if there were not any enrollable/upgradeable ones.
            filtered_course_runs = all_course_runs

        if filtered_course_runs:
            current_course_run = get_closest_course_run(filtered_course_runs)
    return current_course_run