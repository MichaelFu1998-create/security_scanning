def do_url_scheme(parser, token):
    """
    Generates a &lt;link&gt; tag with oembed autodiscovery bits.

    {% oembed_url_scheme %}
    """
    args = token.split_contents()
    if len(args) != 1:
        raise template.TemplateSyntaxError('%s takes no parameters.' % args[0])
    return OEmbedURLSchemeNode()