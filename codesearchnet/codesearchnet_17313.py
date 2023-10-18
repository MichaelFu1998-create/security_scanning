def boilerplate(name, contact, description, pmids, version, copyright, authors, licenses, disclaimer, output):
    """Build a template BEL document with the given PubMed identifiers."""
    from .document_utils import write_boilerplate

    write_boilerplate(
        name=name,
        version=version,
        description=description,
        authors=authors,
        contact=contact,
        copyright=copyright,
        licenses=licenses,
        disclaimer=disclaimer,
        pmids=pmids,
        file=output,
    )