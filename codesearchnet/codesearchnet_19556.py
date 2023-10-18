def enum(name, *members, **withvalue):
    """class buider"""
    if len(members) == 1:
        if isinstance(members[0], str):
            members = members[0].split()
        elif isinstance(members[0], (list, tuple)):
            members = members[0]

    dic = {v: v for v in members}
    dic.update(withvalue)

    return type(name, (Enum,), dic)