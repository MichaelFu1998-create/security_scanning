def interleaves(self, info):
        """Does the buffer interleave with this one?"""
        return info.byte_offset == self.component_type.size * self.components