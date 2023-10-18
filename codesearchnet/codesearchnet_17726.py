def _sendBit(port, bit):
    """Send an individual bit to the FireCracker module usr RTS/DTR."""
    if bit == '0':
        _setRTSDTR(port, 0, 1)
    elif bit == '1':
        _setRTSDTR(port, 1, 0)
    else:
        return
    time.sleep(bitDelay)
    _setRTSDTR(port, 1, 1)
    time.sleep(bitDelay)