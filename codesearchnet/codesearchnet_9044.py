def parse_description(markdown=True):
    """
    Parse the description in the README file
    """
    if markdown: return parse_markdown()

    try:
        from pypandoc import convert

        readme_file = f'{PACKAGE_ROOT}/docs/index.rst'
        if not path.exists(readme_file):
            raise ImportError
        return convert(readme_file, 'rst')

    except ImportError:
        return parse_markdown()