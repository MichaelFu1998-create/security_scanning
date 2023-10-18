def write_boilerplate(name: str,
                      version: Optional[str] = None,
                      description: Optional[str] = None,
                      authors: Optional[str] = None,
                      contact: Optional[str] = None,
                      copyright: Optional[str] = None,
                      licenses: Optional[str] = None,
                      disclaimer: Optional[str] = None,
                      namespace_url: Optional[Mapping[str, str]] = None,
                      namespace_patterns: Optional[Mapping[str, str]] = None,
                      annotation_url: Optional[Mapping[str, str]] = None,
                      annotation_patterns: Optional[Mapping[str, str]] = None,
                      annotation_list: Optional[Mapping[str, Set[str]]] = None,
                      pmids: Optional[Iterable[Union[str, int]]] = None,
                      entrez_ids: Optional[Iterable[Union[str, int]]] = None,
                      file: Optional[TextIO] = None,
                      ) -> None:
    """Write a boilerplate BEL document, with standard document metadata, definitions.

    :param name: The unique name for this BEL document
    :param contact: The email address of the maintainer
    :param description: A description of the contents of this document
    :param authors: The authors of this document
    :param version: The version. Defaults to current date in format ``YYYYMMDD``.
    :param copyright: Copyright information about this document
    :param licenses: The license applied to this document
    :param disclaimer: The disclaimer for this document
    :param namespace_url: an optional dictionary of {str name: str URL} of namespaces
    :param namespace_patterns: An optional dictionary of {str name: str regex} namespaces
    :param annotation_url: An optional dictionary of {str name: str URL} of annotations
    :param annotation_patterns: An optional dictionary of {str name: str regex} of regex annotations
    :param annotation_list: An optional dictionary of {str name: set of names} of list annotations
    :param pmids: A list of PubMed identifiers to auto-populate with citation and abstract
    :param entrez_ids: A list of Entrez identifiers to autopopulate the gene summary as evidence
    :param file: A writable file or file-like. If None, defaults to :data:`sys.stdout`
    """
    lines = make_knowledge_header(
        name=name,
        version=version or '1.0.0',
        description=description,
        authors=authors,
        contact=contact,
        copyright=copyright,
        licenses=licenses,
        disclaimer=disclaimer,
        namespace_url=namespace_url,
        namespace_patterns=namespace_patterns,
        annotation_url=annotation_url,
        annotation_patterns=annotation_patterns,
        annotation_list=annotation_list,
    )

    for line in lines:
        print(line, file=file)

    if pmids is not None:
        for line in make_pubmed_abstract_group(pmids):
            print(line, file=file)

    if entrez_ids is not None:
        for line in make_pubmed_gene_group(entrez_ids):
            print(line, file=file)