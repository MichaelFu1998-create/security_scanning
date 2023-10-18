def dropbox_form(request):
    """ generates a dropbox uid and renders the submission form with a signed version of that id"""
    from briefkasten import generate_post_token
    token = generate_post_token(secret=request.registry.settings['post_secret'])
    return dict(
        action=request.route_url('dropbox_form_submit', token=token),
        fileupload_url=request.route_url('dropbox_fileupload', token=token),
        **defaults(request))