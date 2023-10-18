def get_earliest_start_date_from_program(program):
    """
    Get the earliest date that one of the courses in the program was available.
    For the sake of emails to new learners, we treat this as the program start date.

    Arguemnts:
        program (dict): Program data from Course Catalog API

    returns:
        datetime.datetime: The date and time at which the first course started
    """
    start_dates = []
    for course in program.get('courses', []):
        for run in course.get('course_runs', []):
            if run.get('start'):
                start_dates.append(parse_lms_api_datetime(run['start']))
    if not start_dates:
        return None
    return min(start_dates)