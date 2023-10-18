def set_trace(context):
    """
    Start a pdb set_trace inside of the template with the context available as
    'context'. Uses ipdb if available.
    """
    try:
        import ipdb as pdb
    except ImportError:
        import pdb
        print("For best results, pip install ipdb.")
    print("Variables that are available in the current context:")
    render = lambda s: template.Template(s).render(context)
    availables = get_variables(context)
    pprint(availables)
    print('Type `availables` to show this list.')
    print('Type <variable_name> to access one.')
    print('Use render("template string") to test template rendering')
    # Cram context variables into the local scope
    for var in availables:
        locals()[var] = context[var]
    pdb.set_trace()
    return ''