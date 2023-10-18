def add(self, operator, *args):
        """Adds a proximal operator to the list of operators"""

        if isinstance(operator, str):
            op = getattr(proxops, operator)(*args)
        elif isinstance(operator, proxops.ProximalOperatorBaseClass):
            op = operator
        else:
            raise ValueError("operator must be a string or a subclass of ProximalOperator")

        self.operators.append(op)
        return self