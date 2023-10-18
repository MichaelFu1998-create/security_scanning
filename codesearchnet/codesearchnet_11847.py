def get_previous_thumbprint(self, components=None):
        """
        Returns a dictionary representing the previous configuration state.

        Thumbprint is of the form:

            {
                component_name1: {key: value},
                component_name2: {key: value},
                ...
            }

        """
        components = str_to_component_list(components)
        tp_fn = self.manifest_filename
        tp_text = None
        if self.file_exists(tp_fn):
            fd = six.BytesIO()
            get(tp_fn, fd)
            tp_text = fd.getvalue()
            manifest_data = {}
            raw_data = yaml.load(tp_text)
            for k, v in raw_data.items():
                manifest_key = assert_valid_satchel(k)
                service_name = clean_service_name(k)
                if components and service_name not in components:
                    continue
                manifest_data[manifest_key] = v
            return manifest_data