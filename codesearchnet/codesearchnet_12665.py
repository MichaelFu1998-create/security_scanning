def parse_field(self, field, field_value):
        """ Parse the operators and traduce: ES to SQLAlchemy operators """
        if type(field_value) is dict:
            # TODO: check operators and emit error
            operator = list(field_value)[0]
            if self.verify_operator(operator) is False:
                return "Error: operator does not exist", operator
            value = field_value[operator]
        elif type(field_value) is unicode:
            operator = u'equals'
            value = field_value
        return field, operator, value