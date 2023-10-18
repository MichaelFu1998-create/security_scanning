def photos(context, path):
    """Adds images to the last article"""

    config = context.obj

    header('Looking for the latest article...')
    article_filename = find_last_article(config['CONTENT_DIR'])
    if not article_filename:
        return click.secho('No articles.', fg='red')
    click.echo(os.path.basename(article_filename))

    header('Looking for images...')
    images = list(sorted(find_images(path)))
    if not images:
        return click.secho('Found no images.', fg='red')

    for filename in images:
        click.secho(filename, fg='green')

    if not click.confirm('\nAdd these images to the latest article'):
        abort(config)

    url_prefix = os.path.join('{filename}', IMAGES_PATH)
    images_dir = os.path.join(config['CONTENT_DIR'], IMAGES_PATH)
    os.makedirs(images_dir, exist_ok=True)

    header('Processing images...')
    urls = []
    for filename in images:
        image_basename = os.path.basename(filename).replace(' ', '-').lower()
        urls.append(os.path.join(url_prefix, image_basename))
        image_filename = os.path.join(images_dir, image_basename)
        print(filename, image_filename)
        import_image(filename, image_filename)

    content = '\n'
    for url in urls:
        url = url.replace('\\', '/')
        content += '\n![image description]({})\n'.format(url)

    header('Adding to article: {}'.format(article_filename))
    with click.open_file(article_filename, 'a') as f:
        f.write(content)
    click.launch(article_filename)