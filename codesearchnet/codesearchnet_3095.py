def argsplit(args, sep=','):
    """used to split JS args (it is not that simple as it seems because
       sep can be inside brackets).

       pass args *without* brackets!

       Used also to parse array and object elements, and more"""
    parsed_len = 0
    last = 0
    splits = []
    for e in bracket_split(args, brackets=['()', '[]', '{}']):
        if e[0] not in {'(', '[', '{'}:
            for i, char in enumerate(e):
                if char == sep:
                    splits.append(args[last:parsed_len + i])
                    last = parsed_len + i + 1
        parsed_len += len(e)
    splits.append(args[last:])
    return splits