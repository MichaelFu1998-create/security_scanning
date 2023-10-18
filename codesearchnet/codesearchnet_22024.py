def path(self, a_hash, b_hash):
        """Return nodes in the path between 'a' and 'b' going from
        parent to child NOT including 'a' """

        def _path(a, b):
            if a is b:
                return [a]
            else:
                assert len(a.children) == 1
                return [a] + _path(a.children[0], b)

        a = self.nodes[a_hash]
        b = self.nodes[b_hash]
        return _path(a, b)[1:]