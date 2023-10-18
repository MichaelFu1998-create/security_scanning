def _validate_ram(ram_in_mb):
    """Rounds ram up to the nearest multiple of _MEMORY_MULTIPLE."""
    return int(GoogleV2CustomMachine._MEMORY_MULTIPLE * math.ceil(
        ram_in_mb / GoogleV2CustomMachine._MEMORY_MULTIPLE))