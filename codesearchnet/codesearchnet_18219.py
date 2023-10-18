def _handle_field_value(self, field, value):
        """ Handle the field, value pair. """
        if field == 'event':
            self._event = value
        elif field == 'data':
            self._data_lines.append(value)
        elif field == 'id':
            # Not implemented
            pass
        elif field == 'retry':
            # Not implemented
            pass