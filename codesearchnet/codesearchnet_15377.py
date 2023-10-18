def _validate_license(model):
    """Given the model, check the license is one valid for publication."""
    license_mapping = obtain_licenses()
    try:
        license_url = model.metadata['license_url']
    except KeyError:
        raise exceptions.MissingRequiredMetadata('license_url')
    try:
        license = license_mapping[license_url]
    except KeyError:
        raise exceptions.InvalidLicense(license_url)
    if not license['is_valid_for_publication']:
        raise exceptions.InvalidLicense(license_url)