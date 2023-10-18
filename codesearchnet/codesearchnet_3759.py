def populate_resource_columns(item_dict):
        """Operates on item_dict

        Promotes the resource_name and resource_type fields to the
        top-level of the serialization so they can be printed as columns.
        Also makes a copies name field to type, which is a default column."""
        item_dict['type'] = item_dict['name']
        if len(item_dict['summary_fields']) == 0:
            # Singleton roles omit these fields
            item_dict['resource_name'] = None
            item_dict['resource_type'] = None
        else:
            sf = item_dict['summary_fields']
            # Explination of fallback state:
            # The situation where resource_name or resource_type is not present
            # should not be seen for singleton roles, and where it is seen,
            # there may be a problem with data quality on the server
            item_dict['resource_name'] = sf.get('resource_name', '[unknown]')
            item_dict['resource_type'] = sf.get('resource_type', '[unknown]')