def new_post():
    """Touch a new post in src/"""
    logger.info(new_post.__doc__)
    # make the new post's filename
    now = datetime.datetime.now()
    now_s = now.strftime('%Y-%m-%d-%H-%M')
    filepath = join(Post.src_dir, now_s + src_ext)
    # check if `src/` exists
    if not exists(Post.src_dir):
        logger.error(SourceDirectoryNotFound.__doc__)
        sys.exit(SourceDirectoryNotFound.exit_code)
    # write sample content to new post
    content = (
        'Title\n'
        'Title Picture URL\n'
        '---\n'
        'Markdown content ..'
    )
    f = open(filepath, 'w')
    f.write(content)
    f.close()
    logger.success('New post created: %s' % filepath)