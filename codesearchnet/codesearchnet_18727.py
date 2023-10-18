def do_oembed(parser, token):
    """
    A node which parses everything between its two nodes, and replaces any links
    with OEmbed-provided objects, if possible.

    Supports two optional argument, which is the maximum width and height,
    specified like so:

    {% oembed 640x480 %}http://www.viddler.com/explore/SYSTM/videos/49/{% endoembed %}

    and or the name of a sub tempalte directory to render templates from:

    {% oembed 320x240 in "comments" %}http://www.viddler.com/explore/SYSTM/videos/49/{% endoembed %}

    or:

    {% oembed in "comments" %}http://www.viddler.com/explore/SYSTM/videos/49/{% endoembed %}

    either of those will render templates in oembed/comments/oembedtype.html

    Additionally, you can specify a context variable to drop the rendered text in:

    {% oembed 600x400 in "comments" as var_name %}...{% endoembed %}
    {% oembed as var_name %}...{% endoembed %}
    """
    args = token.split_contents()
    template_dir = None
    var_name = None
    if len(args) > 2:
        if len(args) == 3 and args[1] == 'in':
            template_dir = args[2]
        elif len(args) == 3 and args[1] == 'as':
            var_name = args[2]
        elif len(args) == 4 and args[2] == 'in':
            template_dir = args[3]
        elif len(args) == 4 and args[2] == 'as':
            var_name = args[3]
        elif len(args) == 6 and args[4] == 'as':
            template_dir = args[3]
            var_name = args[5]
        else:
            raise template.TemplateSyntaxError("OEmbed either takes a single " \
                "(optional) argument: WIDTHxHEIGHT, where WIDTH and HEIGHT " \
                "are positive integers, and or an optional 'in " \
                " \"template_dir\"' argument set.")
        if template_dir:
            if not (template_dir[0] == template_dir[-1] and template_dir[0] in ('"', "'")):
                raise template.TemplateSyntaxError("template_dir must be quoted")
            template_dir = template_dir[1:-1]

    if len(args) >= 2 and 'x' in args[1]:
        width, height = args[1].lower().split('x')
        if not width and height:
            raise template.TemplateSyntaxError("OEmbed's optional WIDTHxHEIGH" \
                "T argument requires WIDTH and HEIGHT to be positive integers.")
    else:
        width, height = None, None
    nodelist = parser.parse(('endoembed',))
    parser.delete_first_token()
    return OEmbedNode(nodelist, width, height, template_dir, var_name)