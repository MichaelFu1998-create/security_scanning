def make_pubmed_abstract_group(pmids: Iterable[Union[str, int]]) -> Iterable[str]:
    """Build a skeleton for the citations' statements.
    
    :param pmids: A list of PubMed identifiers
    :return: An iterator over the lines of the citation section
    """
    for pmid in set(pmids):
        yield ''

        res = requests.get(title_url_fmt.format(pmid))
        title = res.content.decode('utf-8').strip()

        yield 'SET Citation = {{"{}", "{}"}}'.format(title, pmid)

        res = requests.get(abstract_url_fmt.format(pmid))
        abstract = res.content.decode('utf-8').strip()

        yield 'SET Evidence = "{}"'.format(abstract)
        yield '\nUNSET Evidence\nUNSET Citation'