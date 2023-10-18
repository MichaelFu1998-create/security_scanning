def can_connect_to(self, other):
        """Whether a connection can be established between those two meshes."""
        assert other.is_mesh()
        disconnected = not other.is_connected() and not self.is_connected()
        types_differ = self._is_consumed_mesh() != other._is_consumed_mesh()
        return disconnected and types_differ