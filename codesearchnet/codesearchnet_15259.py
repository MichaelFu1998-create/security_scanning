def dropbox_post_factory(request):
    """receives a UUID via the request and returns either a fresh or an existing dropbox
    for it"""
    try:
        max_age = int(request.registry.settings.get('post_token_max_age_seconds'))
    except Exception:
        max_age = 300

    try:
        drop_id = parse_post_token(
            token=request.matchdict['token'],
            secret=request.registry.settings['post_secret'],
            max_age=max_age)
    except SignatureExpired:
        raise HTTPGone('dropbox expired')
    except Exception:  # don't be too specific on the reason for the error
        raise HTTPNotFound('no such dropbox')
    dropbox = request.registry.settings['dropbox_container'].get_dropbox(drop_id)
    if dropbox.status_int >= 20:
        raise HTTPGone('dropbox already in processing, no longer accepts data')
    return dropbox