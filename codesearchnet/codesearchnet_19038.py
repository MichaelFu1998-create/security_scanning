def social_widget_render(parser, token):
    """ Renders the selected social widget. You can specify optional settings
    that will be passed  to widget template.

    Sample usage:
    {% social_widget_render widget_template ke1=val1 key2=val2 %}

    For example to render Twitter follow button you can use code like this:
    {% social_widget_render 'twitter/follow_button.html' username="ev" %}
    """
    bits = token.split_contents()
    tag_name = bits[0]

    if len(bits) < 2:
        raise TemplateSyntaxError("'%s' takes at least one argument" %
                                  tag_name)
    args = []
    kwargs = {}

    bits = bits[1:]

    if len(bits):
        for bit in bits:
            match = kwarg_re.match(bit)
            if not match:
                raise TemplateSyntaxError("Malformed arguments to %s tag" %
                                          tag_name)
            name, value = match.groups()

            if name:
                # Replacing hyphens with underscores because
                # variable names cannot contain hyphens.
                name = name.replace('-', '_')
                kwargs[name] = parser.compile_filter(value)
            else:
                args.append(parser.compile_filter(value))

    return SocialWidgetNode(args, kwargs)