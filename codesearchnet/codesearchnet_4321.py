def load_license_list(file_name):
    """
    Return the licenses list version tuple and a mapping of licenses
    name->id and id->name loaded from a JSON file
    from https://github.com/spdx/license-list-data
    """
    licenses_map = {}
    with codecs.open(file_name, 'rb', encoding='utf-8') as lics:
        licenses = json.load(lics)
        version = licenses['licenseListVersion'].split('.')
        for lic in licenses['licenses']:
            if lic.get('isDeprecatedLicenseId'):
                continue
            name = lic['name']
            identifier = lic['licenseId']
            licenses_map[name] = identifier
            licenses_map[identifier] = name
    return version, licenses_map