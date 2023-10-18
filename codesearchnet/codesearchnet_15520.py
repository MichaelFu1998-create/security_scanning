def operate(self, left, right, operation):
        """ Do operation on colors
        args:
            left (str): left side
            right (str): right side
            operation (str): Operation
        returns:
            str
        """
        operation = {
            '+': operator.add,
            '-': operator.sub,
            '*': operator.mul,
            '/': operator.truediv
        }.get(operation)
        return operation(left, right)