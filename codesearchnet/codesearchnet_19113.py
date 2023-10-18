def is_categorical_type(ary):
    "Checks whether the array is either integral or boolean."
    ary = np.asanyarray(ary)
    return is_integer_type(ary) or ary.dtype.kind == 'b'