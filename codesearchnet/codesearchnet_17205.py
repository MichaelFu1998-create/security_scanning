def spia_matrices_to_tsvs(spia_matrices: Mapping[str, pd.DataFrame], directory: str) -> None:
    """Export a SPIA data dictionary into a directory as several TSV documents."""
    os.makedirs(directory, exist_ok=True)
    for relation, df in spia_matrices.items():
        df.to_csv(os.path.join(directory, f'{relation}.tsv'), index=True)