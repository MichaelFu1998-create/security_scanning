def delete_record(self, instance):
        """Deletes the record."""
        adapter = self.get_adapter_from_instance(instance)
        adapter.delete_record(instance)