def get_order(tre):
    """
    return tree order
    """
    anode = tre.tree&">A"
    sister = anode.get_sisters()[0]
    sisters = (anode.name[1:], sister.name[1:])
    others = [i for i in list("ABCD") if i not in sisters]
    return sorted(sisters) + sorted(others)