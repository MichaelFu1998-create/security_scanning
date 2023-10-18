def parse_markdown():
    """
    Parse markdown as description
    """
    readme_file = f'{PACKAGE_ROOT}/README.md'
    if path.exists(readme_file):
        with open(readme_file, 'r', encoding='utf-8') as f:
            long_description = f.read()
        return long_description