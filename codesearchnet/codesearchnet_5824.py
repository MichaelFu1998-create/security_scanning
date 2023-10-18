def oauth2_authorize(request):
    """ View to start the OAuth2 Authorization flow.

     This view starts the OAuth2 authorization flow. If scopes is passed in
     as a  GET URL parameter, it will authorize those scopes, otherwise the
     default scopes specified in settings. The return_url can also be
     specified as a GET parameter, otherwise the referer header will be
     checked, and if that isn't found it will return to the root path.

    Args:
       request: The Django request object.

    Returns:
         A redirect to Google OAuth2 Authorization.
    """
    return_url = request.GET.get('return_url', None)
    if not return_url:
        return_url = request.META.get('HTTP_REFERER', '/')

    scopes = request.GET.getlist('scopes', django_util.oauth2_settings.scopes)
    # Model storage (but not session storage) requires a logged in user
    if django_util.oauth2_settings.storage_model:
        if not request.user.is_authenticated():
            return redirect('{0}?next={1}'.format(
                settings.LOGIN_URL, parse.quote(request.get_full_path())))
        # This checks for the case where we ended up here because of a logged
        # out user but we had credentials for it in the first place
        else:
            user_oauth = django_util.UserOAuth2(request, scopes, return_url)
            if user_oauth.has_credentials():
                return redirect(return_url)

    flow = _make_flow(request=request, scopes=scopes, return_url=return_url)
    auth_url = flow.step1_get_authorize_url()
    return shortcuts.redirect(auth_url)