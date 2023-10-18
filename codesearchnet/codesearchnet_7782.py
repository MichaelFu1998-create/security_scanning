def check_install(config_data):
    """
    Here we do some **really** basic environment sanity checks.

    Basically we test for the more delicate and failing-prone dependencies:
     * database driver
     * Pillow image format support

    Many other errors will go undetected
    """
    errors = []

    # PIL tests
    try:
        from PIL import Image

        try:
            im = Image.open(os.path.join(os.path.dirname(__file__), '../share/test_image.png'))
            im.load()
        except IOError:  # pragma: no cover
            errors.append(
                'Pillow is not compiled with PNG support, see "Libraries installation issues" '
                'documentation section: https://djangocms-installer.readthedocs.io/en/latest/'
                'libraries.html.'
            )
        try:
            im = Image.open(os.path.join(os.path.dirname(__file__), '../share/test_image.jpg'))
            im.load()
        except IOError:  # pragma: no cover
            errors.append(
                'Pillow is not compiled with JPEG support, see "Libraries installation issues" '
                'documentation section: https://djangocms-installer.readthedocs.io/en/latest/'
                'libraries.html'
            )
    except ImportError:  # pragma: no cover
        errors.append(
            'Pillow is not installed check for installation errors and see "Libraries installation'
            ' issues" documentation section: https://djangocms-installer.readthedocs.io/en/latest/'
            'libraries.html'
        )

    # PostgreSQL test
    if config_data.db_driver == 'psycopg2' and not config_data.no_db_driver:  # pragma: no cover
        try:
            import psycopg2  # NOQA
        except ImportError:
            errors.append(
                'PostgreSQL driver is not installed, but you configured a PostgreSQL database, '
                'please check your installation and see "Libraries installation issues" '
                'documentation section: https://djangocms-installer.readthedocs.io/en/latest/'
                'libraries.html'
            )

    # MySQL test
    if config_data.db_driver == 'mysqlclient' and not config_data.no_db_driver:  # pragma: no cover  # NOQA
        try:
            import MySQLdb  # NOQA
        except ImportError:
            errors.append(
                'MySQL driver is not installed, but you configured a MySQL database, please check '
                'your installation and see "Libraries installation issues" documentation section: '
                'https://djangocms-installer.readthedocs.io/en/latest/libraries.html'
            )
    if errors:  # pragma: no cover
        raise EnvironmentError('\n'.join(errors))