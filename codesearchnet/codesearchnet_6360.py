def _parse_annotations(sbase):
    """Parses cobra annotations from a given SBase object.

    Annotations are dictionaries with the providers as keys.

    Parameters
    ----------
    sbase : libsbml.SBase
        SBase from which the SBML annotations are read

    Returns
    -------
    dict (annotation dictionary)

    FIXME: annotation format must be updated (this is a big collection of
          fixes) - see: https://github.com/opencobra/cobrapy/issues/684)
    """
    annotation = {}

    # SBO term
    if sbase.isSetSBOTerm():
        # FIXME: correct handling of annotations
        annotation["sbo"] = sbase.getSBOTermID()

    # RDF annotation
    cvterms = sbase.getCVTerms()
    if cvterms is None:
        return annotation

    for cvterm in cvterms:  # type: libsbml.CVTerm
        for k in range(cvterm.getNumResources()):
            # FIXME: read and store the qualifier

            uri = cvterm.getResourceURI(k)
            match = URL_IDENTIFIERS_PATTERN.match(uri)
            if not match:
                LOGGER.warning("%s does not conform to "
                               "http(s)://identifiers.org/collection/id", uri)
                continue

            provider, identifier = match.group(1), match.group(2)
            if provider in annotation:
                if isinstance(annotation[provider], string_types):
                    annotation[provider] = [annotation[provider]]
                # FIXME: use a list
                if identifier not in annotation[provider]:
                    annotation[provider].append(identifier)
            else:
                # FIXME: always in list
                annotation[provider] = identifier

    return annotation