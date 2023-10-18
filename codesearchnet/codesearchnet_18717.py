def license_is_oa(license):
    """Return True if license is compatible with Open Access"""
    for oal in OA_LICENSES:
        if re.search(oal, license):
            return True
    return False