def write_document(document, out, validate=True):
    """
    Write an SPDX tag value document.
    - document - spdx.document instance.
    - out - file like object that will be written to.
    Optionally `validate` the document before writing and raise
    InvalidDocumentError if document.validate returns False.
    """
    messages = []
    messages = document.validate(messages)
    if validate and messages:
        raise InvalidDocumentError(messages)

    # Write out document information
    out.write('# Document Information\n\n')
    write_value('SPDXVersion', str(document.version), out)
    write_value('DataLicense', document.data_license.identifier, out)
    write_value('DocumentName', document.name, out)
    write_value('SPDXID', 'SPDXRef-DOCUMENT', out)
    write_value('DocumentNamespace', document.namespace, out)
    if document.has_comment:
        write_text_value('DocumentComment', document.comment, out)
    for doc_ref in document.ext_document_references:
        doc_ref_str = ' '.join([doc_ref.external_document_id,
                                doc_ref.spdx_document_uri,
                                doc_ref.check_sum.identifier + ':' +
                                doc_ref.check_sum.value])
        write_value('ExternalDocumentRef', doc_ref_str, out)
    write_separators(out)
    # Write out creation info
    write_creation_info(document.creation_info, out)
    write_separators(out)

    # Writesorted reviews
    for review in sorted(document.reviews):
        write_review(review, out)
        write_separators(out)

    #Write sorted annotations
    for annotation in sorted(document.annotations):
        write_annotation(annotation, out)
        write_separators(out)

    # Write out package info
    write_package(document.package, out)
    write_separators(out)

    out.write('# Extracted Licenses\n\n')
    for lic in sorted(document.extracted_licenses):
        write_extracted_licenses(lic, out)
        write_separators(out)