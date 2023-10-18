def _get_tuple(self, fields):
    """
    :param fields: a list which contains either 0,1,or 2 values
    :return: a tuple with default values of '';
    """
    v1 = ''
    v2 = ''
    if len(fields) > 0:
      v1 = fields[0]
    if len(fields) > 1:
      v2 = fields[1]
    return v1, v2