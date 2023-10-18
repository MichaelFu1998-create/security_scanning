def projects(ctx, page):
    """List bookmarked projects for user.

    Uses [Caching](/references/polyaxon-cli/#caching)

    Examples:

    \b
    ```bash
    $ polyaxon bookmark projects
    ```

    \b
    ```bash
    $ polyaxon bookmark -u adam projects
    ```
    """
    user = get_username_or_local(ctx.obj.get('username'))

    page = page or 1
    try:
        response = PolyaxonClient().bookmark.projects(username=user, page=page)
    except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
        Printer.print_error(
            'Could not get bookmarked projects for user `{}`.'.format(user))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    meta = get_meta_response(response)
    if meta:
        Printer.print_header('Bookmarked projects for user `{}`.'.format(user))
        Printer.print_header('Navigation:')
        dict_tabulate(meta)
    else:
        Printer.print_header('No bookmarked projects found for user `{}`.'.format(user))

    objects = [Printer.add_status_color(o.to_light_dict(humanize_values=True))
               for o in response['results']]
    objects = list_dicts_to_tabulate(objects)
    if objects:
        Printer.print_header("Projects:")
        dict_tabulate(objects, is_list_dict=True)