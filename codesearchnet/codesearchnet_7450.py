def get_version():
    """Get LanguageTool version."""
    version = _get_attrib().get('version')
    if not version:
        match = re.search(r"LanguageTool-?.*?(\S+)$", get_directory())
        if match:
            version = match.group(1)
    return version