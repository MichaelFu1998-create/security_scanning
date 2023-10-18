def parse_time(block_time):
    """Take a string representation of time from the blockchain, and parse it
       into datetime object.
    """
    return datetime.strptime(block_time, timeFormat).replace(tzinfo=timezone.utc)