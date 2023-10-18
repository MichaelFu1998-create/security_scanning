def output_error(msg):
    """
    Prints the specified string to ``stderr``.

    :param msg: the message to print
    :type msg: str
    """

    click.echo(click.style(msg, fg='red'), err=True)