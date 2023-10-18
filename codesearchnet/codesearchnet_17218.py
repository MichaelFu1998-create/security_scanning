def get_entrez_gene_data(entrez_ids: Iterable[Union[str, int]]):
    """Get gene info from Entrez."""
    url = PUBMED_GENE_QUERY_URL.format(','.join(str(x).strip() for x in entrez_ids))
    response = requests.get(url)
    tree = ElementTree.fromstring(response.content)

    return {
        element.attrib['uid']: {
            'summary': _sanitize(element.find('Summary').text),
            'description': element.find('Description').text
        }
        for element in tree.findall('./DocumentSummarySet/DocumentSummary')
    }