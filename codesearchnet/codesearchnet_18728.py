def do_autodiscover(parser, token):
    """
    Generates a &lt;link&gt; tag with oembed autodiscovery bits for an object.

    {% oembed_autodiscover video %}
    """
    args = token.split_contents()
    if len(args) != 2:
        raise template.TemplateSyntaxError('%s takes an object as its parameter.' % args[0])
    else:
        obj = args[1]
    return OEmbedAutodiscoverNode(obj)