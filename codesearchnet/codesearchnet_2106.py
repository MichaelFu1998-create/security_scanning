def np_dtype(dtype):
    """Translates dtype specifications in configurations to numpy data types.
    Args:
        dtype: String describing a numerical type (e.g. 'float') or numerical type primitive.

    Returns: Numpy data type

    """
    if dtype == 'float' or dtype == float or dtype == np.float32 or dtype == tf.float32:
        return np.float32
    elif dtype == np.float64 or dtype == tf.float64:
        return np.float64
    elif dtype == np.float16 or dtype == tf.float16:
        return np.float16
    elif dtype == 'int' or dtype == int or dtype == np.int32 or dtype == tf.int32:
        return np.int32
    elif dtype == np.int64 or dtype == tf.int64:
        return np.int64
    elif dtype == np.int16 or dtype == tf.int16:
        return np.int16
    elif dtype == 'bool' or dtype == bool or dtype == np.bool_ or dtype == tf.bool:
        return np.bool_
    else:
        raise TensorForceError("Error: Type conversion from type {} not supported.".format(str(dtype)))