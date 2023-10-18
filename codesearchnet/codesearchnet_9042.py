def parse_version(package):
    """
    Parse versions
    """
    init_file = f'{PACKAGE_ROOT}/{package}/__init__.py'
    with open(init_file, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            if '__version__' in line:
                return line.split('=')[1].strip()[1:-1]
    return ''