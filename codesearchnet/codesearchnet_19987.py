def to_table(args, vdims=[]):
    "Helper function to convet an Args object to a HoloViews Table"
    if not Table:
        return "HoloViews Table not available"
    kdims = [dim for dim in args.constant_keys + args.varying_keys
             if dim not in vdims]
    items = [tuple([spec[k] for k in kdims+vdims])
             for spec in args.specs]
    return Table(items, kdims=kdims, vdims=vdims)