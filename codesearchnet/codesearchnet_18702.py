def fix_dashes(string):
    """Fix bad Unicode special dashes in string."""
    string = string.replace(u'\u05BE', '-')
    string = string.replace(u'\u1806', '-')
    string = string.replace(u'\u2E3A', '-')
    string = string.replace(u'\u2E3B', '-')
    string = unidecode(string)
    return re.sub(r'--+', '-', string)