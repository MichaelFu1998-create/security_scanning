def deploy_blog():
    """Deploy new blog to current directory"""
    logger.info(deploy_blog.__doc__)
    # `rsync -aqu path/to/res/* .`
    call(
        'rsync -aqu ' + join(dirname(__file__), 'res', '*') + ' .',
        shell=True)
    logger.success('Done')
    logger.info('Please edit config.toml to meet your needs')