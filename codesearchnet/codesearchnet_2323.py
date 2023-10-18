def FindControl(control: Control, compare: Callable, maxDepth: int = 0xFFFFFFFF, findFromSelf: bool = False, foundIndex: int = 1) -> Control:
    """
    control: `Control` or its subclass.
    compare: compare function with parameters (control: Control, depth: int) which returns bool.
    maxDepth: int, enum depth.
    findFromSelf: bool, if False, do not compare self.
    foundIndex: int, starts with 1, >= 1.
    Return `Control` subclass or None if not find.
    """
    foundCount = 0
    if not control:
        control = GetRootControl()
    traverseCount = 0
    for child, depth in WalkControl(control, findFromSelf, maxDepth):
        traverseCount += 1
        if compare(child, depth):
            foundCount += 1
            if foundCount == foundIndex:
                child.traverseCount = traverseCount
                return child