def abstract_equality_comparison(self, other):
        ''' returns the result of JS == compare.
           result is PyJs type: bool'''
        tx, ty = self.TYPE, other.TYPE
        if tx == ty:
            if tx == 'Undefined' or tx == 'Null':
                return true
            if tx == 'Number' or tx == 'String' or tx == 'Boolean':
                return Js(self.value == other.value)
            return Js(self is other)  # Object
        elif (tx == 'Undefined' and ty == 'Null') or (ty == 'Undefined'
                                                      and tx == 'Null'):
            return true
        elif tx == 'Number' and ty == 'String':
            return self.abstract_equality_comparison(other.to_number())
        elif tx == 'String' and ty == 'Number':
            return self.to_number().abstract_equality_comparison(other)
        elif tx == 'Boolean':
            return self.to_number().abstract_equality_comparison(other)
        elif ty == 'Boolean':
            return self.abstract_equality_comparison(other.to_number())
        elif (tx == 'String' or tx == 'Number') and other.is_object():
            return self.abstract_equality_comparison(other.to_primitive())
        elif (ty == 'String' or ty == 'Number') and self.is_object():
            return self.to_primitive().abstract_equality_comparison(other)
        else:
            return false