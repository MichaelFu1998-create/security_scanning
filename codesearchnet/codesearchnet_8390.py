def dump(buf, indent=0, skip=""):
    """Dump UnionType/StructType to STDOUT"""
    if not isinstance(type(buf), (type(Union), type(Structure))):
        raise RuntimeError("Error type(%s)" % type(buf))

    for field in getattr(buf, '_fields_'):
        name, types = field[0], field[1]
        if name in skip:
            return
        value = getattr(buf, name)

        if isinstance(types, (type(Union), type(Structure))):
            cij.info("%s%s:" % (" " * indent, name))
            dump(value, indent+2, skip)
        elif isinstance(types, type(Array)):
            for i, item in enumerate(value):
                name_index = "%s[%s]" % (name, i)

                if isinstance(types, (type(Union), type(Structure))):
                    cij.info("%s%s:" % (" " * indent, name_index))
                    dump(item, indent + 2, skip)
                else:
                    cij.info("%s%-12s: 0x%x" % (" " * indent, name_index, item))
        else:
            cij.info("%s%-12s: 0x%x" % (" " * indent, name, value))