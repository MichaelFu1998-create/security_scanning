def _process_filters(filter_dictionary):
    """
    We have a filter_dictionary - this means that if the field is included
    and matches, then we can include, OR if the field is undefined, then we
    assume it is safe to include
    """
    def filter_item(field):
        """ format elasticsearch filter to pass if value matches OR field is not included """
        if filter_dictionary[field] is not None:
            return {
                "or": [
                    _get_filter_field(field, filter_dictionary[field]),
                    {
                        "missing": {
                            "field": field
                        }
                    }
                ]
            }

        return {
            "missing": {
                "field": field
            }
        }

    return [filter_item(field) for field in filter_dictionary]