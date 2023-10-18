def grant(username):
    """Grant superuser role to a user.

    Example:

    \b
    ```bash
    $ polyaxon superuser grant david
    ```
    """
    try:
        PolyaxonClient().user.grant_superuser(username)
    except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
        Printer.print_error('Could not grant superuser role to user `{}`.'.format(username))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    Printer.print_success(
        "Superuser role was granted successfully to user `{}`.".format(username))