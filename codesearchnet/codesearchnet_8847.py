def is_course_run_upgradeable(course_run):
    """
    Return true if the course run has a verified seat with an unexpired upgrade deadline, false otherwise.
    """
    now = datetime.datetime.now(pytz.UTC)
    for seat in course_run.get('seats', []):
        if seat.get('type') == 'verified':
            upgrade_deadline = parse_datetime_handle_invalid(seat.get('upgrade_deadline'))
            return not upgrade_deadline or upgrade_deadline > now
    return False