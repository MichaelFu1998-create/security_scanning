def print_information(handler, label):
    """
    Prints latest tag's information
    """
    click.echo('=> Latest stable: {tag}'.format(
        tag=click.style(str(handler.latest_stable or 'N/A'), fg='yellow' if
                        handler.latest_stable else 'magenta')
    ))

    if label is not None:
        latest_revision = handler.latest_revision(label)
        click.echo('=> Latest relative revision ({label}): {tag}'.format(
            label=click.style(label, fg='blue'),
            tag=click.style(str(latest_revision or 'N/A'),
                                fg='yellow' if latest_revision else 'magenta')
        ))