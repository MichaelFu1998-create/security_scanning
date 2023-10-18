def dropbox_factory(request):
    """ expects the id of an existing dropbox and returns its instance"""
    try:
        return request.registry.settings['dropbox_container'].get_dropbox(request.matchdict['drop_id'])
    except KeyError:
        raise HTTPNotFound('no such dropbox')