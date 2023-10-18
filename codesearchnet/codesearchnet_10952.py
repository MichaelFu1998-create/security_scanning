def prepare_attrib_mapping(self, primitive):
        """Pre-parse buffer mappings for each VBO to detect interleaved data for a primitive"""
        buffer_info = []
        for name, accessor in primitive.attributes.items():
            info = VBOInfo(*accessor.info())
            info.attributes.append((name, info.components))

            if buffer_info and buffer_info[-1].buffer_view == info.buffer_view:
                if buffer_info[-1].interleaves(info):
                    buffer_info[-1].merge(info)
                    continue

            buffer_info.append(info)

        return buffer_info