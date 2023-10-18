def spia_matrices_to_excel(spia_matrices: Mapping[str, pd.DataFrame], path: str) -> None:
    """Export a SPIA data dictionary into an Excel sheet at the given path.

    .. note::

        # The R import should add the values:
        # ["nodes"] from the columns
        # ["title"] from the name of the file
        # ["NumberOfReactions"] set to "0"
    """
    writer = pd.ExcelWriter(path, engine='xlsxwriter')

    for relation, df in spia_matrices.items():
        df.to_excel(writer, sheet_name=relation, index=False)

    # Save excel
    writer.save()