def get_field_value(self, field_key):
        """
        Given field_key will return value held at self.model_instance.  If
        model_instance has not been provided will return None.
        """

        def get_value(document, field_key):
            # Short circuit the function if we do not have a document
            if document is None:
                return None

            current_key, new_key_array = trim_field_key(document, field_key)
            key_array_digit = int(new_key_array[-1]) if new_key_array and has_digit(new_key_array) else None
            new_key = make_key(new_key_array)

            if key_array_digit is not None and len(new_key_array) > 0:
                # Handleing list fields
                if len(new_key_array) == 1:
                    return_data = document._data.get(current_key, [])
                elif isinstance(document, BaseList):
                    return_list = []
                    if len(document) > 0:
                        return_list = [get_value(doc, new_key) for doc in document]
                    return_data = return_list
                else:
                    return_data = get_value(getattr(document, current_key), new_key)

            elif len(new_key_array) > 0:
                return_data = get_value(document._data.get(current_key), new_key)
            else:
                # Handeling all other fields and id
                try: # Added try except otherwise we get "TypeError: getattr(): attribute name must be string" error from mongoengine/base/datastructures.py 
                    return_data = (document._data.get(None, None) if current_key == "id" else
                              document._data.get(current_key, None))
                except: 
                    return_data = document._data.get(current_key, None)

            return return_data

        if self.is_initialized:
            return get_value(self.model_instance, field_key)
        else:
            return None