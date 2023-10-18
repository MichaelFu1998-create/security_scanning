def get_deploy_funcs(components, current_thumbprint, previous_thumbprint, preview=False):
    """
    Returns a generator yielding the named functions needed for a deployment.
    """
    for component in components:
        funcs = manifest_deployers.get(component, [])
        for func_name in funcs:

            #TODO:remove this after burlap.* naming prefix bug fixed
            if func_name.startswith('burlap.'):
                print('skipping %s' % func_name)
                continue

            takes_diff = manifest_deployers_takes_diff.get(func_name, False)

            func = resolve_deployer(func_name)
            current = current_thumbprint.get(component)
            last = previous_thumbprint.get(component)
            if takes_diff:
                yield func_name, partial(func, last=last, current=current)
            else:
                yield func_name, partial(func)