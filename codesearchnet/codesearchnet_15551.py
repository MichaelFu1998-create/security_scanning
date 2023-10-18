def operate(self, vala, valb, oper):
        """Perform operation
        args:
            vala (mixed): 1st value
            valb (mixed): 2nd value
            oper (str): operation
        returns:
            mixed
        """
        operation = {
            '+': operator.add,
            '-': operator.sub,
            '*': operator.mul,
            '/': operator.truediv,
            '=': operator.eq,
            '>': operator.gt,
            '<': operator.lt,
            '>=': operator.ge,
            '=<': operator.le,
        }.get(oper)
        if operation is None:
            raise SyntaxError("Unknown operation %s" % oper)
        ret = operation(vala, valb)
        if oper in '+-*/' and int(ret) == ret:
            ret = int(ret)
        return ret