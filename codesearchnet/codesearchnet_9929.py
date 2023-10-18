def bootstrap_paginate(parser, token):
    """
    Renders a Page object as a Twitter Bootstrap styled pagination bar.
    Compatible with Bootstrap 3.x and 4.x only.

    Example::

        {% bootstrap_paginate page_obj range=10 %}


    Named Parameters::

        range - The size of the pagination bar (ie, if set to 10 then, at most,
                10 page numbers will display at any given time) Defaults to
                None, which shows all pages.


        size - Accepts "small", and "large". Defaults to
                    None which is the standard size.

        show_prev_next - Accepts "true" or "false". Determines whether or not
                        to show the previous and next page links. Defaults to
                        "true"


        show_first_last - Accepts "true" or "false". Determines whether or not
                          to show the first and last page links. Defaults to
                          "false"

        previous_label - The text to display for the previous page link.
                         Defaults to "&larr;"

        next_label - The text to display for the next page link. Defaults to
                     "&rarr;"

        first_label - The text to display for the first page link. Defaults to
                      "&laquo;"

        last_label - The text to display for the last page link. Defaults to
                     "&raquo;"

        url_view_name - The named URL to use. Defaults to None. If None, then the
                        default template simply appends the url parameter as a
                        relative URL link, eg: <a href="?page=1">1</a>

        url_param_name - The name of the parameter to use in the URL. If
                         url_view_name is set to None, this string is used as the
                         parameter name in the relative URL path. If a URL
                         name is specified, this string is used as the
                         parameter name passed into the reverse() method for
                         the URL.

        url_extra_args - This is used only in conjunction with url_view_name.
                         When referencing a URL, additional arguments may be
                         passed in as a list.

        url_extra_kwargs - This is used only in conjunction with url_view_name.
                           When referencing a URL, additional named arguments
                           may be passed in as a dictionary.

        url_get_params - The other get parameters to pass, only the page
                         number will be overwritten. Use this to preserve
                         filters.

        url_anchor - The anchor to use in URLs. Defaults to None.

        extra_pagination_classes - A space separated list of CSS class names
                                   that will be added to the top level <ul>
                                   HTML element. In particular, this can be
                                   utilized in Bootstrap 4 installatinos  to
                                   add the appropriate alignment classes from
                                   Flexbox utilites, eg:  justify-content-center
    """
    bits = token.split_contents()
    if len(bits) < 2:
        raise TemplateSyntaxError("'%s' takes at least one argument"
                                  " (Page object reference)" % bits[0])
    page = parser.compile_filter(bits[1])
    kwargs = {}
    bits = bits[2:]

    kwarg_re = re.compile(r'(\w+)=(.+)')

    if len(bits):
        for bit in bits:
            match = kwarg_re.match(bit)
            if not match:
                raise TemplateSyntaxError("Malformed arguments to bootstrap_pagination paginate tag")
            name, value = match.groups()
            kwargs[name] = parser.compile_filter(value)

    return BootstrapPaginationNode(page, kwargs)