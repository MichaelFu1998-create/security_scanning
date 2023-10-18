def render_to_string(template, extra=None):
    """
    Renders the given template to a string.
    """
    from jinja2 import Template
    extra = extra or {}
    final_fqfn = find_template(template)
    assert final_fqfn, 'Template not found: %s' % template
    template_content = open(final_fqfn, 'r').read()
    t = Template(template_content)
    if extra:
        context = env.copy()
        context.update(extra)
    else:
        context = env
    rendered_content = t.render(**context)
    rendered_content = rendered_content.replace('&quot;', '"')
    return rendered_content