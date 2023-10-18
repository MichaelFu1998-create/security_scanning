def _setRTSDTR(port, RTS, DTR):
    """Set RTS and DTR to the requested state."""
    port.setRTS(RTS)
    port.setDTR(DTR)