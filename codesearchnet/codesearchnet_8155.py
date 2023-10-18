def wheel_helper(pos, length, cycle_step):
    """Helper for wheel_color that distributes colors over length and
    allows shifting position."""
    return wheel_color((pos * len(_WHEEL) / length) + cycle_step)