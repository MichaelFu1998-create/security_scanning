def abstract_equality_op(self, other):
    ''' returns the result of JS == compare.
       result is PyJs type: bool'''
    tx, ty = Type(self), Type(other)
    if tx == ty:
        if tx == 'Undefined' or tx == 'Null':
            return True
        if tx == 'Number' or tx == 'String' or tx == 'Boolean':
            return self == other
        return self is other  # Object
    elif (tx == 'Undefined' and ty == 'Null') or (ty == 'Undefined'
                                                  and tx == 'Null'):
        return True
    elif tx == 'Number' and ty == 'String':
        return abstract_equality_op(self, to_number(other))
    elif tx == 'String' and ty == 'Number':
        return abstract_equality_op(to_number(self), other)
    elif tx == 'Boolean':
        return abstract_equality_op(to_number(self), other)
    elif ty == 'Boolean':
        return abstract_equality_op(self, to_number(other))
    elif (tx == 'String' or tx == 'Number') and is_object(other):
        return abstract_equality_op(self, to_primitive(other))
    elif (ty == 'String' or ty == 'Number') and is_object(self):
        return abstract_equality_op(to_primitive(self), other)
    else:
        return False