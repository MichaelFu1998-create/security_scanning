def oauth_required(decorated_function=None, scopes=None, **decorator_kwargs):
    """ Decorator to require OAuth2 credentials for a view.


    .. code-block:: python
       :caption: views.py
       :name: views_required_2


       from oauth2client.django_util.decorators import oauth_required

       @oauth_required
       def requires_default_scopes(request):
          email = request.credentials.id_token['email']
          service = build(serviceName='calendar', version='v3',
                       http=request.oauth.http,
                       developerKey=API_KEY)
          events = service.events().list(
                                    calendarId='primary').execute()['items']
          return HttpResponse(
              "email: {0}, calendar: {1}".format(email, str(events)))

    Args:
        decorated_function: View function to decorate, must have the Django
           request object as the first argument.
        scopes: Scopes to require, will default.
        decorator_kwargs: Can include ``return_url`` to specify the URL to
           return to after OAuth2 authorization is complete.

    Returns:
        An OAuth2 Authorize view if credentials are not found or if the
        credentials are missing the required scopes. Otherwise,
        the decorated view.
    """
    def curry_wrapper(wrapped_function):
        @wraps(wrapped_function)
        def required_wrapper(request, *args, **kwargs):
            if not (django_util.oauth2_settings.storage_model is None or
                    request.user.is_authenticated()):
                redirect_str = '{0}?next={1}'.format(
                    django.conf.settings.LOGIN_URL,
                    parse.quote(request.path))
                return shortcuts.redirect(redirect_str)

            return_url = decorator_kwargs.pop('return_url',
                                              request.get_full_path())
            user_oauth = django_util.UserOAuth2(request, scopes, return_url)
            if not user_oauth.has_credentials():
                return shortcuts.redirect(user_oauth.get_authorize_redirect())
            setattr(request, django_util.oauth2_settings.request_prefix,
                    user_oauth)
            return wrapped_function(request, *args, **kwargs)

        return required_wrapper

    if decorated_function:
        return curry_wrapper(decorated_function)
    else:
        return curry_wrapper