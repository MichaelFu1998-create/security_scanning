def wtime_to_minutes(time_string):
    ''' wtime_to_minutes

    Convert standard wallclock time string to minutes.

    Args:
        - Time_string in HH:MM:SS format

    Returns:
        (int) minutes

    '''
    hours, mins, seconds = time_string.split(':')
    total_mins = int(hours) * 60 + int(mins)
    if total_mins < 1:
        logger.warning("Time string '{}' parsed to {} minutes, less than 1".format(time_string, total_mins))
    return total_mins