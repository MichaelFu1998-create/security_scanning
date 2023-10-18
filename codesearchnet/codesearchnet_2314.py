def WalkTree(top, getChildren: Callable = None, getFirstChild: Callable = None, getNextSibling: Callable = None, yieldCondition: Callable = None, includeTop: bool = False, maxDepth: int = 0xFFFFFFFF):
    """
    Walk a tree not using recursive algorithm.
    top: a tree node.
    getChildren: function(treeNode) -> list.
    getNextSibling: function(treeNode) -> treeNode.
    getNextSibling: function(treeNode) -> treeNode.
    yieldCondition: function(treeNode, depth) -> bool.
    includeTop: bool, if True yield top first.
    maxDepth: int, enum depth.

    If getChildren is valid, ignore getFirstChild and getNextSibling,
        yield 3 items tuple: (treeNode, depth, remain children count in current depth).
    If getChildren is not valid, using getFirstChild and getNextSibling,
        yield 2 items tuple: (treeNode, depth).
    If yieldCondition is not None, only yield tree nodes that yieldCondition(treeNode, depth)->bool returns True.

    For example:
    def GetDirChildren(dir_):
        if os.path.isdir(dir_):
            return [os.path.join(dir_, it) for it in os.listdir(dir_)]
    for it, depth, leftCount in WalkTree('D:\\', getChildren= GetDirChildren):
        print(it, depth, leftCount)
    """
    if maxDepth <= 0:
        return
    depth = 0
    if getChildren:
        if includeTop:
            if not yieldCondition or yieldCondition(top, 0):
                yield top, 0, 0
        children = getChildren(top)
        childList = [children]
        while depth >= 0:   #or while childList:
            lastItems = childList[-1]
            if lastItems:
                if not yieldCondition or yieldCondition(lastItems[0], depth + 1):
                    yield lastItems[0], depth + 1, len(lastItems) - 1
                if depth + 1 < maxDepth:
                    children = getChildren(lastItems[0])
                    if children:
                        depth += 1
                        childList.append(children)
                del lastItems[0]
            else:
                del childList[depth]
                depth -= 1
    elif getFirstChild and getNextSibling:
        if includeTop:
            if not yieldCondition or yieldCondition(top, 0):
                yield top, 0
        child = getFirstChild(top)
        childList = [child]
        while depth >= 0:  #or while childList:
            lastItem = childList[-1]
            if lastItem:
                if not yieldCondition or yieldCondition(lastItem, depth + 1):
                    yield lastItem, depth + 1
                child = getNextSibling(lastItem)
                childList[depth] = child
                if depth + 1 < maxDepth:
                    child = getFirstChild(lastItem)
                    if child:
                        depth += 1
                        childList.append(child)
            else:
                del childList[depth]
                depth -= 1