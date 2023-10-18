def set(self, **kwargs):
        """
        Set input values on task

        Args:
               arbitrary_keys: values for the keys

        Returns:
            None
        """
        for port_name, port_value in kwargs.items():
            # Support both port and port.value
            if hasattr(port_value, 'value'):
                port_value = port_value.value

            self.inputs.__setattr__(port_name, port_value)