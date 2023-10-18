def xpath_eval(node, extra_ns=None):
    """
    Returns an XPathEvaluator, with namespace prefixes 'bpmn' for
    http://www.omg.org/spec/BPMN/20100524/MODEL, and additional specified ones
    """
    namespaces = {'bpmn': BPMN_MODEL_NS}
    if extra_ns:
        namespaces.update(extra_ns)
    return lambda path: node.findall(path, namespaces)