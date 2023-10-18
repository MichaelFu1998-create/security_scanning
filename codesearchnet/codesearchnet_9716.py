def set_process_timezone(TZ):
    """
    Parameters
    ----------
    TZ: string
    """
    try:
        prev_timezone = os.environ['TZ']
    except KeyError:
        prev_timezone = None
    os.environ['TZ'] = TZ
    time.tzset()  # Cause C-library functions to notice the update.
    return prev_timezone