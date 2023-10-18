def make_pubmed_gene_group(entrez_ids: Iterable[Union[str, int]]) -> Iterable[str]:
    """Builds a skeleton for gene summaries

    :param entrez_ids: A list of Entrez Gene identifiers to query the PubMed service
    :return: An iterator over statement lines for NCBI Entrez Gene summaries
    """
    url = PUBMED_GENE_QUERY_URL.format(','.join(str(x).strip() for x in entrez_ids))
    response = requests.get(url)
    tree = ElementTree.fromstring(response.content)

    for x in tree.findall('./DocumentSummarySet/DocumentSummary'):
        yield '\n# {}'.format(x.find('Description').text)
        yield 'SET Citation = {{"Other", "PubMed Gene", "{}"}}'.format(x.attrib['uid'])
        yield 'SET Evidence = "{}"'.format(x.find('Summary').text.strip().replace('\n', ''))
        yield '\nUNSET Evidence\nUNSET Citation'