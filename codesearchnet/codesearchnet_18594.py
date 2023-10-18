def oembed_schema(request):
    """
    A site profile detailing valid endpoints for a given domain.  Allows for
    better auto-discovery of embeddable content.

    OEmbed-able content lives at a URL that maps to a provider.
    """
    current_domain = Site.objects.get_current().domain
    url_schemes = [] # a list of dictionaries for all the urls we can match
    endpoint = reverse('oembed_json') # the public endpoint for our oembeds
    providers = oembed.site.get_providers()

    for provider in providers:
        # first make sure this provider class is exposed at the public endpoint
        if not provider.provides:
            continue
        
        match = None
        if isinstance(provider, DjangoProvider):
            # django providers define their regex_list by using urlreversing
            url_pattern = resolver.reverse_dict.get(provider._meta.named_view)

            # this regex replacement is set to be non-greedy, which results
            # in things like /news/*/*/*/*/ -- this is more explicit
            if url_pattern:
                regex = re.sub(r'%\(.+?\)s', '*', url_pattern[0][0][0])
                match = 'http://%s/%s' % (current_domain, regex)
        elif isinstance(provider, HTTPProvider):
            match = provider.url_scheme
        else:
            match = provider.regex

        if match:
            url_schemes.append({
                'type': provider.resource_type,
                'matches': match,
                'endpoint': endpoint
            })
    
    url_schemes.sort(key=lambda item: item['matches'])
    
    response = HttpResponse(mimetype='application/json')
    response.write(simplejson.dumps(url_schemes))
    return response