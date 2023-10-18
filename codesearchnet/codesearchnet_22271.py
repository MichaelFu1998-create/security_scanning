def confirm(tag):
    """
    Prompts user before proceeding
    """
    click.echo()
    if click.confirm('Do you want to create the tag {tag}?'.format(
            tag=click.style(str(tag), fg='yellow')),
        default=True, abort=True):
        git.create_tag(tag)

    if click.confirm(
        'Do you want to push the tag {tag} into the upstream?'.format(
            tag=click.style(str(tag), fg='yellow')),
        default=True):
        git.push_tag(tag)
        click.echo('Done!')
    else:
        git.delete_tag(tag)
        click.echo('Aborted!')