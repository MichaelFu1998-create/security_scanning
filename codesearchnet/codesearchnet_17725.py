def _sendBinaryData(port, data):
    """Send a string of binary data to the FireCracker with proper timing.

    See the diagram in the spec referenced above for timing information.
    The module level variables leadInOutDelay and bitDelay represent how
    long each type of delay should be in seconds. They may require tweaking
    on some setups.
    """
    _reset(port)
    time.sleep(leadInOutDelay)
    for digit in data:
        _sendBit(port, digit)
    time.sleep(leadInOutDelay)