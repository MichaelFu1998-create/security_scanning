def deposit_links_factory(pid):
    """Factory for record links generation.

    The dictionary is formed as:

    .. code-block:: python

        {
            'files': '/url/to/files',
            'publish': '/url/to/publish',
            'edit': '/url/to/edit',
            'discard': '/url/to/discard',
            ...
        }

    :param pid: The record PID object.
    :returns: A dictionary that contains all the links.
    """
    links = default_links_factory(pid)

    def _url(name, **kwargs):
        """URL builder."""
        endpoint = '.{0}_{1}'.format(
            current_records_rest.default_endpoint_prefixes[pid.pid_type],
            name,
        )
        return url_for(endpoint, pid_value=pid.pid_value, _external=True,
                       **kwargs)

    links['files'] = _url('files')

    ui_endpoint = current_app.config.get('DEPOSIT_UI_ENDPOINT')
    if ui_endpoint is not None:
        links['html'] = ui_endpoint.format(
            host=request.host,
            scheme=request.scheme,
            pid_value=pid.pid_value,
        )

    deposit_cls = Deposit
    if 'pid_value' in request.view_args:
        deposit_cls = request.view_args['pid_value'].data[1].__class__

    for action in extract_actions_from_class(deposit_cls):
        links[action] = _url('actions', action=action)
    return links