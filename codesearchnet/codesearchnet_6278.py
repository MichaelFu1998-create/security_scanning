def _cell(x):
    """translate an array x into a MATLAB cell array"""
    x_no_none = [i if i is not None else "" for i in x]
    return array(x_no_none, dtype=np_object)