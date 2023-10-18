def add_control_number(self, tag, value):
        """Add a control-number 00x for given tag with value."""
        record_add_field(self.record,
                         tag,
                         controlfield_value=value)