def cellsiter_to_dataframe(cellsiter, args, drop_allna=True):
    """Convert multiple cells to a frame.

    If args is an empty sequence, all values are included.
    If args is specified, cellsiter must have shareable parameters.

    Args:
        cellsiter: A mapping from cells names to CellsImpl objects.
        args: A sequence of arguments
    """
    from modelx.core.cells import shareable_parameters

    if len(args):
        indexes = shareable_parameters(cellsiter)
    else:
        indexes = get_all_params(cellsiter.values())

    result = None

    for cells in cellsiter.values():
        df = cells_to_dataframe(cells, args)

        if drop_allna and df.isnull().all().all():
            continue  #  Ignore all NA or empty

        if df.index.names != [None]:
            if isinstance(df.index, pd.MultiIndex):
                if _pd_ver < (0, 20):
                    df = _reset_naindex(df)

            df = df.reset_index()

        missing_params = set(indexes) - set(df)

        for params in missing_params:
            df[params] = np.nan

        if result is None:
            result = df
        else:
            try:
                result = pd.merge(result, df, how="outer")
            except MergeError:
                # When no common column exists, i.e. all cells are scalars.
                result = pd.concat([result, df], axis=1)
            except ValueError:
                # When common columns are not coercible (numeric vs object),
                # Make the numeric column object type
                cols = set(result.columns) & set(df.columns)
                for col in cols:

                    # When only either of them has object dtype
                    if (
                        len(
                            [
                                str(frame[col].dtype)
                                for frame in (result, df)
                                if str(frame[col].dtype) == "object"
                            ]
                        )
                        == 1
                    ):

                        if str(result[col].dtype) == "object":
                            frame = df
                        else:
                            frame = result
                        frame[[col]] = frame[col].astype("object")

                # Try again
                result = pd.merge(result, df, how="outer")

    if result is None:
        return pd.DataFrame()
    else:
        return result.set_index(indexes) if indexes else result