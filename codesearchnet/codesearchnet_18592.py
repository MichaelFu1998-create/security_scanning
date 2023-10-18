def json(request, *args, **kwargs):
    """
    The oembed endpoint, or the url to which requests for metadata are passed.
    Third parties will want to access this view with URLs for your site's
    content and be returned OEmbed metadata.
    """
    # coerce to dictionary
    params = dict(request.GET.items())
    
    callback = params.pop('callback', None)
    url = params.pop('url', None)
    
    if not url:
        return HttpResponseBadRequest('Required parameter missing: URL')
    
    try:
        provider = oembed.site.provider_for_url(url)
        if not provider.provides:
            raise OEmbedMissingEndpoint()
    except OEmbedMissingEndpoint:
        raise Http404('No provider found for %s' % url)
    
    query = dict([(smart_str(k), smart_str(v)) for k, v in params.items() if v])
    
    try:
        resource = oembed.site.embed(url, **query)
    except OEmbedException, e:
        raise Http404('Error embedding %s: %s' % (url, str(e)))

    response = HttpResponse(mimetype='application/json')
    json = resource.json
    
    if callback:
        response.write('%s(%s)' % (defaultfilters.force_escape(callback), json))
    else:
        response.write(json)
    
    return response