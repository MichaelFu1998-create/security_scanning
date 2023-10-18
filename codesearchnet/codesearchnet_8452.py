def dev_get_chunk(dev_name, state, pugrp=None, punit=None):
    """
    Get a chunk-descriptor for the first chunk in the given state.

    If the pugrp and punit is set, then search only that pugrp/punit

    @returns the first chunk in the given state if one exists, None otherwise
    """

    rprt = dev_get_rprt(dev_name, pugrp, punit)
    if not rprt:
        return None

    return next((d for d in rprt if d["cs"] == state), None)