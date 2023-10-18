def in_op(self, other):
    '''checks if self is in other'''
    if not is_object(other):
        raise MakeError(
            'TypeError',
            "You can\'t use 'in' operator to search in non-objects")
    return other.has_property(to_string(self))