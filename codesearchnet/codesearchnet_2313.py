def CreatePattern(patternId: int, pattern: ctypes.POINTER(comtypes.IUnknown)):
    """Create a concreate pattern by pattern id and pattern(POINTER(IUnknown))."""
    subPattern = pattern.QueryInterface(GetPatternIdInterface(patternId))
    if subPattern:
        return PatternConstructors[patternId](pattern=subPattern)