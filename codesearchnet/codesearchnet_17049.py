def get_nift_values() -> Mapping[str, str]:
    """Extract the list of NIFT names from the BEL resource and builds a dictionary mapping from the lowercased version
    to the uppercase version.
    """
    r = get_bel_resource(NIFT)
    return {
        name.lower(): name
        for name in r['Values']
    }