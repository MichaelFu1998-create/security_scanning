def revoke(username):
    """Revoke superuser role to a user.

    Example:

    \b
    ```bash
    $ polyaxon superuser revoke david
    ```
    """
    try:
        PolyaxonClient().user.revoke_superuser(username)
    except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
        Printer.print_error('Could not revoke superuser role from user `{}`.'.format(username))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    Printer.print_success(
        "Superuser role was revoked successfully from user `{}`.".format(username))