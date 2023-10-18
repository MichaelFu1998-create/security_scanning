def _finish_inheritance(self):
        """Finish those who still need to inherit."""
        while self._inheritance_todos:
            prototype, parent_id = self._inheritance_todos.pop()
            parent = self._id_cache[parent_id]
            prototype.inherit_from(parent)