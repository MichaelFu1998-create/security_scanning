def get_function(function_name):
    """
    Given a Python function name, return the function it refers to.
    """
    module, basename = str(function_name).rsplit('.', 1)
    try:
        return getattr(__import__(module, fromlist=[basename]), basename)
    except (ImportError, AttributeError):
        raise FunctionNotFound(function_name)