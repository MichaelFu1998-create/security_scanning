def dropbox_editor_factory(request):
    """ this factory also requires the editor token"""
    dropbox = dropbox_factory(request)
    if is_equal(dropbox.editor_token, request.matchdict['editor_token'].encode('utf-8')):
        return dropbox
    else:
        raise HTTPNotFound('invalid editor token')