def _remove_failed_items(self, failed_items, items_to_create, items_to_update, items_to_delete):
        """
        Remove content metadata items from the `items_to_create`, `items_to_update`, `items_to_delete` dicts.

        Arguments:
            failed_items (list): Failed Items to be removed.
            items_to_create (dict): dict containing the items created successfully.
            items_to_update (dict): dict containing the items updated successfully.
            items_to_delete (dict): dict containing the items deleted successfully.
        """
        for item in failed_items:
            content_metadata_id = item['courseID']
            items_to_create.pop(content_metadata_id, None)
            items_to_update.pop(content_metadata_id, None)
            items_to_delete.pop(content_metadata_id, None)