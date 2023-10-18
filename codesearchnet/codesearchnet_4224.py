def write_file(spdx_file, out):
    """
    Write a file fields to out.
    """
    out.write('# File\n\n')
    write_value('FileName', spdx_file.name, out)
    write_value('SPDXID', spdx_file.spdx_id, out)
    if spdx_file.has_optional_field('type'):
        write_file_type(spdx_file.type, out)
    write_value('FileChecksum', spdx_file.chk_sum.to_tv(), out)
    if isinstance(spdx_file.conc_lics, (document.LicenseConjunction, document.LicenseDisjunction)):
        write_value('LicenseConcluded', u'({0})'.format(spdx_file.conc_lics), out)
    else:
        write_value('LicenseConcluded', spdx_file.conc_lics, out)

    # write sorted list
    for lics in sorted(spdx_file.licenses_in_file):
        write_value('LicenseInfoInFile', lics, out)

    if isinstance(spdx_file.copyright, six.string_types):
        write_text_value('FileCopyrightText', spdx_file.copyright, out)
    else:
        write_value('FileCopyrightText', spdx_file.copyright, out)

    if spdx_file.has_optional_field('license_comment'):
        write_text_value('LicenseComments', spdx_file.license_comment, out)

    if spdx_file.has_optional_field('comment'):
        write_text_value('FileComment', spdx_file.comment, out)

    if spdx_file.has_optional_field('notice'):
        write_text_value('FileNotice', spdx_file.notice, out)

    for contributor in sorted(spdx_file.contributors):
        write_value('FileContributor', contributor, out)

    for dependency in sorted(spdx_file.dependencies):
        write_value('FileDependency', dependency, out)

    names = spdx_file.artifact_of_project_name
    homepages = spdx_file.artifact_of_project_home
    uris = spdx_file.artifact_of_project_uri

    for name, homepage, uri in sorted(zip_longest(names, homepages, uris)):
        write_value('ArtifactOfProjectName', name, out)
        if homepage is not None:
            write_value('ArtifactOfProjectHomePage', homepage, out)
        if uri is not None:
            write_value('ArtifactOfProjectURI', uri, out)