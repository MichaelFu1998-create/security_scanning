def get_page_url(page_num, current_app, url_view_name, url_extra_args, url_extra_kwargs, url_param_name, url_get_params, url_anchor):
    """
    Helper function to return a valid URL string given the template tag parameters
    """
    if url_view_name is not None:
        # Add page param to the kwargs list. Overrides any previously set parameter of the same name.
        url_extra_kwargs[url_param_name] = page_num

        try:
            url = reverse(url_view_name, args=url_extra_args, kwargs=url_extra_kwargs, current_app=current_app)
        except NoReverseMatch as e:  # Attempt to load view from application root, allowing the use of non-namespaced view names if your view is defined in the root application
            if settings.SETTINGS_MODULE:

                if django.VERSION < (1, 9, 0):
                    separator  = '.'
                else:
                    separator  = ':' # Namespace separator changed to colon after 1.8

                project_name = settings.SETTINGS_MODULE.split('.')[0]
                try:
                    url = reverse(project_name + separator + url_view_name, args=url_extra_args, kwargs=url_extra_kwargs, current_app=current_app)
                except NoReverseMatch:
                    raise e # Raise the original exception so the error message doesn't confusingly include something the Developer didn't add to the view name themselves
            else:
                raise e # We can't determine the project name so just re-throw the exception

    else:
        url = ''
        url_get_params = url_get_params or QueryDict(url)
        url_get_params = url_get_params.copy()
        url_get_params[url_param_name] = str(page_num)

    if len(url_get_params) > 0:
        if not isinstance(url_get_params, QueryDict):
            tmp = QueryDict(mutable=True)
            tmp.update(url_get_params)
            url_get_params = tmp
        url += '?' + url_get_params.urlencode()

    if (url_anchor is not None):
        url += '#' + url_anchor

    return url