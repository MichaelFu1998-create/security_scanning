def get_tensor_dependencies(tensor):
    """
    Utility method to get all dependencies (including placeholders) of a tensor (backwards through the graph).

    Args:
        tensor (tf.Tensor): The input tensor.

    Returns: Set of all dependencies (including needed placeholders) for the input tensor.
    """
    dependencies = set()
    dependencies.update(tensor.op.inputs)
    for sub_op in tensor.op.inputs:
        dependencies.update(get_tensor_dependencies(sub_op))
    return dependencies