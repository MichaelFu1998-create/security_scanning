def WalkControl(control: Control, includeTop: bool = False, maxDepth: int = 0xFFFFFFFF):
    """
    control: `Control` or its subclass.
    includeTop: bool, if True, yield (control, 0) first.
    maxDepth: int, enum depth.
    Yield 2 items tuple(control: Control, depth: int).
    """
    if includeTop:
        yield control, 0
    if maxDepth <= 0:
        return
    depth = 0
    child = control.GetFirstChildControl()
    controlList = [child]
    while depth >= 0:
        lastControl = controlList[-1]
        if lastControl:
            yield lastControl, depth + 1
            child = lastControl.GetNextSiblingControl()
            controlList[depth] = child
            if depth + 1 < maxDepth:
                child = lastControl.GetFirstChildControl()
                if child:
                    depth += 1
                    controlList.append(child)
        else:
            del controlList[depth]
            depth -= 1