def consume_json(request):
    """
    Extract and return oembed content for given urls.

    Required GET params:
        urls - list of urls to consume

    Optional GET params:
        width - maxwidth attribute for oembed content
        height - maxheight attribute for oembed content
        template_dir - template_dir to use when rendering oembed

    Returns:
        list of dictionaries with oembed metadata and renderings, json encoded
    """
    client = OEmbedConsumer()
    
    urls = request.GET.getlist('urls')
    width = request.GET.get('width')
    height = request.GET.get('height')
    template_dir = request.GET.get('template_dir')

    output = {}
    ctx = RequestContext(request)

    for url in urls:
        try:
            provider = oembed.site.provider_for_url(url)
        except OEmbedMissingEndpoint:
            oembeds = None
            rendered = None
        else:
            oembeds = url
            rendered = client.parse_text(url, width, height, context=ctx, template_dir=template_dir)

        output[url] = {
            'oembeds': oembeds,
            'rendered': rendered,
        }

    return HttpResponse(simplejson.dumps(output), mimetype='application/json')