def to_zebra_params(params):
    """
    Transforms the given `params` dict to values that are understood by Zebra (eg. False is represented as 'false')
    """
    def to_zebra_value(value):
        transform_funcs = {
            bool: lambda v: 'true' if v else 'false',
        }

        return transform_funcs.get(type(value), lambda v: v)(value)

    return {param: to_zebra_value(value) for param, value in params.items()}