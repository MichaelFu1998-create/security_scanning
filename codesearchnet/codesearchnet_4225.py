def write_package(package, out):
    """
    Write a package fields to out.
    """
    out.write('# Package\n\n')
    write_value('PackageName', package.name, out)
    if package.has_optional_field('version'):
        write_value('PackageVersion', package.version, out)
    write_value('PackageDownloadLocation', package.download_location, out)

    if package.has_optional_field('summary'):
        write_text_value('PackageSummary', package.summary, out)

    if package.has_optional_field('source_info'):
        write_text_value('PackageSourceInfo', package.source_info, out)

    if package.has_optional_field('file_name'):
        write_value('PackageFileName', package.file_name, out)

    if package.has_optional_field('supplier'):
        write_value('PackageSupplier', package.supplier, out)

    if package.has_optional_field('originator'):
        write_value('PackageOriginator', package.originator, out)

    if package.has_optional_field('check_sum'):
        write_value('PackageChecksum', package.check_sum.to_tv(), out)

    write_value('PackageVerificationCode', format_verif_code(package), out)

    if package.has_optional_field('description'):
        write_text_value('PackageDescription', package.description, out)

    if isinstance(package.license_declared, (document.LicenseConjunction,
        document.LicenseDisjunction)):
        write_value('PackageLicenseDeclared', u'({0})'.format(package.license_declared), out)
    else:
        write_value('PackageLicenseDeclared', package.license_declared, out)

    if isinstance(package.conc_lics, (document.LicenseConjunction,
        document.LicenseDisjunction)):
        write_value('PackageLicenseConcluded', u'({0})'.format(package.conc_lics), out)
    else:
        write_value('PackageLicenseConcluded', package.conc_lics, out)

    # Write sorted list of licenses.
    for lics in sorted(package.licenses_from_files):
        write_value('PackageLicenseInfoFromFiles', lics, out)

    if package.has_optional_field('license_comment'):
        write_text_value('PackageLicenseComments', package.license_comment, out)

    # cr_text is either free form text or NONE or NOASSERTION.
    if isinstance(package.cr_text, six.string_types):
        write_text_value('PackageCopyrightText', package.cr_text, out)
    else:
        write_value('PackageCopyrightText', package.cr_text, out)

    if package.has_optional_field('homepage'):
        write_value('PackageHomePage', package.homepage, out)

    # Write sorted files.
    for spdx_file in sorted(package.files):
        write_separators(out)
        write_file(spdx_file, out)