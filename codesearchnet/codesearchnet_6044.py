def md_dynamic_default_values_info(name, node):
    """Extract metadata Dynamic Default Values from an xml node"""
    configurations = node.find("configurations")
    if configurations is not None:
        configurations = []
        for n in node.findall("configuration"):
            dimension = n.find("dimension")
            dimension = dimension.text if dimension is not None else None
            policy = n.find("policy")
            policy = policy.text if policy is not None else None
            defaultValueExpression = n.find("defaultValueExpression")
            defaultValueExpression = defaultValueExpression.text if defaultValueExpression is not None else None

            configurations.append(DynamicDefaultValuesConfiguration(dimension, policy, defaultValueExpression))

    return DynamicDefaultValues(name, configurations)