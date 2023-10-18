def main(graph: BELGraph, xlsx: str, tsvs: str):
    """Export the graph to a SPIA Excel sheet."""
    if not xlsx and not tsvs:
        click.secho('Specify at least one option --xlsx or --tsvs', fg='red')
        sys.exit(1)

    spia_matrices = bel_to_spia_matrices(graph)

    if xlsx:
        spia_matrices_to_excel(spia_matrices, xlsx)

    if tsvs:
        spia_matrices_to_tsvs(spia_matrices, tsvs)