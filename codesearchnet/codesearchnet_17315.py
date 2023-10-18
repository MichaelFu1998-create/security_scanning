def get_pmids(graph: BELGraph, output: TextIO):
    """Output PubMed identifiers from a graph to a stream."""
    for pmid in get_pubmed_identifiers(graph):
        click.echo(pmid, file=output)