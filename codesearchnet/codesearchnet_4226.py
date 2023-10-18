def write_extracted_licenses(lics, out):
    """
    Write extracted licenses fields to out.
    """
    write_value('LicenseID', lics.identifier, out)

    if lics.full_name is not None:
        write_value('LicenseName', lics.full_name, out)

    if lics.comment is not None:
        write_text_value('LicenseComment', lics.comment, out)

    for xref in sorted(lics.cross_ref):
        write_value('LicenseCrossReference', xref, out)

    write_text_value('ExtractedText', lics.text, out)