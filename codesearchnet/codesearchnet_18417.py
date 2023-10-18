def extract_version_number(string: str) -> str:
    """
    Extracts a version from a string in the form: `.*[0-9]+(_[0-9]+)*.*`, e.g. Irods4_1_9CompatibleController.

    If the string contains multiple version numbers, the first (from left) is extracted.

    Will raise a `ValueError` if there is no version number in the given string.
    :param string: the string containing the version number
    :return: the extracted version
    """
    matched = _EXTRACT_VERSION_PATTERN.search(string)
    if matched is None:
        raise ValueError("No version number in string")
    return matched.group().replace("_", ".")