def get_component_order(component_names):
    """
    Given a list of components, re-orders them according to inter-component dependencies so the most depended upon are first.
    """
    assert isinstance(component_names, (tuple, list))
    component_dependences = {}
    for _name in component_names:
        deps = set(manifest_deployers_befores.get(_name, []))
        deps = deps.intersection(component_names)
        component_dependences[_name] = deps
    component_order = list(topological_sort(component_dependences.items()))
    return component_order