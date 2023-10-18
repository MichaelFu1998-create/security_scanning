def accessor(parser, token):
    """This template tag is used to do complex nested attribute accessing of
    an object.  The first parameter is the object being accessed, subsequent
    paramters are one of: 

    * a variable in the template context
    * a literal in the template context
    * either of the above surrounded in square brackets

    For each variable or literal parameter given a `getattr` is called on the
    object, chaining to the next parameter.  For any sqaure bracket enclosed
    items the access is done through a dictionary lookup.

    Example::

        {% accessor car where 'front_seat' [position] ['fabric'] %}

    The above would result in the following chain of commands:

    .. code-block:: python

        ref = getattr(car, where)
        ref = getattr(ref, 'front_seat')
        ref = ref[position]
        return ref['fabric']

    This tag also supports "as" syntax, putting the results into a template
    variable::

        {% accessor car 'interior' as foo %}
    """
    contents = token.split_contents()
    tag = contents[0]
    if len(contents) < 3:
        raise template.TemplateSyntaxError(('%s requires at least two '
            'arguments: object and one or more getattr parms') % tag)

    as_var = None
    if len(contents) >= 4:
        # check for "as" syntax
        if contents[-2] == 'as':
            as_var = contents[-1]
            contents = contents[:-2]

    return AccessorNode(contents[1], contents[2:], as_var)