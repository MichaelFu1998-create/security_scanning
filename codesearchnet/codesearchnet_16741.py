def cells_to_series(cells, args):
    """Convert a CellImpl into a Series.

    `args` must be a sequence of argkeys.

    `args` can be longer or shorter then the number of cell's parameters.
    If shorter, then defaults are filled if any, else raise error.
    If longer, then redundant args are ignored.
    """

    paramlen = len(cells.formula.parameters)
    is_multidx = paramlen > 1

    if len(cells.data) == 0:
        data = {}
        indexes = None

    elif paramlen == 0:  # Const Cells
        data = list(cells.data.values())
        indexes = [np.nan]

    else:

        if len(args) > 0:
            defaults = tuple(
                param.default
                for param in cells.formula.signature.parameters.values()
            )
            updated_args = []
            for arg in args:

                if len(arg) > paramlen:
                    arg = arg[:paramlen]
                elif len(arg) < paramlen:
                    arg += defaults[len(arg) :]

                updated_args.append(arg)

            items = [
                (arg, cells.data[arg])
                for arg in updated_args
                if arg in cells.data
            ]
        else:
            items = [(key, value) for key, value in cells.data.items()]

        if not is_multidx:  # Peel 1-element tuple
            items = [(key[0], value) for key, value in items]

        if len(items) == 0:
            indexes, data = None, {}
        else:
            indexes, data = zip(*items)
            if is_multidx:
                indexes = pd.MultiIndex.from_tuples(indexes)

    result = pd.Series(data=data, name=cells.name, index=indexes)

    if indexes is not None and any(i is not np.nan for i in indexes):
        result.index.names = list(cells.formula.parameters)

    return result