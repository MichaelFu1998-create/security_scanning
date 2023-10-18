def whoami():
    """Show current logged Polyaxon user."""
    try:
        user = PolyaxonClient().auth.get_user()
    except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
        Printer.print_error('Could not load user info.')
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)
    click.echo("\nUsername: {username}, Email: {email}\n".format(**user.to_dict()))