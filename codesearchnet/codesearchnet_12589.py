def add_condition(self, field_name, op, value):
        """
        Add a query condition and validate it.
        raise ParamsException if failed.
        self.view required
        :param field_name:
        :param op:
        :param value:
        :return: None
        """
        if not isinstance(op, SQL_OP):
            if op not in SQL_OP.txt2op:
                raise SQLOperatorInvalid(op)
            else:
                op = SQL_OP.txt2op.get(op)
        self.conditions.append([field_name, op, value])