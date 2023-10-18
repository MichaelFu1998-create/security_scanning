def get_languages() -> set:
    """Get supported languages."""
    try:
        languages = cache['languages']
    except KeyError:
        languages = LanguageTool._get_languages()
        cache['languages'] = languages
    return languages