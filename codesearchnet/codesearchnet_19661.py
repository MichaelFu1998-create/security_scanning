def clean():
    """Clean htmls rux built: `rm -rf post page index.html`"""
    logger.info(clean.__doc__)
    paths = ['post', 'page', 'index.html']
    call(['rm', '-rf'] + paths)
    logger.success('Done')