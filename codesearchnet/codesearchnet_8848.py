def get_closest_course_run(course_runs):
    """
    Return course run with start date closest to now.
    """
    if len(course_runs) == 1:
        return course_runs[0]

    now = datetime.datetime.now(pytz.UTC)
    # course runs with no start date should be considered last.
    never = now - datetime.timedelta(days=3650)
    return min(course_runs, key=lambda x: abs(get_course_run_start(x, never) - now))