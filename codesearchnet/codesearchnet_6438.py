def _descriptor_changed(self, descriptor):
        """Called when the specified descriptor has changed its value."""
        # Tell the descriptor it has a new value to read.
        desc = descriptor_list().get(descriptor)
        if desc is not None:
            desc._value_read.set()