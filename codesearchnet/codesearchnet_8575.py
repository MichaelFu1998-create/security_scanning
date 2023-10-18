def transmit(self, payload, **kwargs):
        """
        Transmit content metadata items to the integrated channel.
        """
        items_to_create, items_to_update, items_to_delete, transmission_map = self._partition_items(payload)
        self._transmit_delete(items_to_delete)
        self._transmit_create(items_to_create)
        self._transmit_update(items_to_update, transmission_map)