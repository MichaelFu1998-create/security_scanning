def compare(buf_a, buf_b, ignore):
    """Compare of two Buffer item"""
    for field in getattr(buf_a, '_fields_'):
        name, types = field[0], field[1]

        if name in ignore:
            continue

        val_a = getattr(buf_a, name)
        val_b = getattr(buf_b, name)

        if isinstance(types, (type(Union), type(Structure))):
            if compare(val_a, val_b, ignore):
                return 1
        elif isinstance(types, type(Array)):
            for i, _ in enumerate(val_a):
                if isinstance(types, (type(Union), type(Structure))):
                    if compare(val_a[i], val_b[i], ignore):
                        return 1
                else:
                    if val_a[i] != val_b[i]:
                        return 1
        else:
            if val_a != val_b:
                return 1

    return 0