def _check_mappings(self, doc_type, body):
        """
        We desire to index content so that anything we want to be textually searchable(and therefore needing to be
        analysed), but the other fields are designed to be filters, and only require an exact match. So, we want to
        set up the mappings for these fields as "not_analyzed" - this will allow our filters to work faster because
        they only have to work off exact matches
        """

        # Make fields other than content be indexed as unanalyzed terms - content
        # contains fields that are to be analyzed
        exclude_fields = ["content"]
        field_properties = getattr(settings, "ELASTIC_FIELD_MAPPINGS", {})

        def field_property(field_name, field_value):
            """
            Prepares field as property syntax for providing correct mapping desired for field

            Mappings format in elasticsearch is as follows:
            {
               "doc_type": {
                  "properties": {
                     "nested_property": {
                        "properties": {
                           "an_analysed_property": {
                              "type": "string"
                           },
                           "another_analysed_property": {
                              "type": "string"
                           }
                        }
                     },
                     "a_not_analysed_property": {
                        "type": "string",
                        "index": "not_analyzed"
                     },
                     "a_date_property": {
                        "type": "date"
                     }
                  }
               }
            }

            We can only add new ones, but the format is the same
            """
            prop_val = None
            if field_name in field_properties:
                prop_val = field_properties[field_name]
            elif isinstance(field_value, dict):
                props = {fn: field_property(fn, field_value[fn]) for fn in field_value}
                prop_val = {"properties": props}
            else:
                prop_val = {
                    "type": "string",
                    "index": "not_analyzed",
                }

            return prop_val

        new_properties = {
            field: field_property(field, value)
            for field, value in body.items()
            if (field not in exclude_fields) and (field not in self._get_mappings(doc_type).get('properties', {}))
        }

        if new_properties:
            self._es.indices.put_mapping(
                index=self.index_name,
                doc_type=doc_type,
                body={
                    doc_type: {
                        "properties": new_properties,
                    }
                }
            )
            self._clear_mapping(doc_type)