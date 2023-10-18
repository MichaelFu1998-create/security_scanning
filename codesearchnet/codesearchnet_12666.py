def create_query(self, attr):
        """ Mix all values and make the query """
        field = attr[0]
        operator = attr[1]
        value = attr[2]
        model = self.model

        if '.' in field:
            field_items = field.split('.')
            field_name = getattr(model, field_items[0], None)
            class_name = field_name.property.mapper.class_
            new_model = getattr(class_name, field_items[1])
            return field_name.has(OPERATORS[operator](new_model, value))

        return OPERATORS[operator](getattr(model, field, None), value)