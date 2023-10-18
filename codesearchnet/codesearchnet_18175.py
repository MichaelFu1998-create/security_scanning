def _generate_circle(self):
        """Generates the circle.
        """
        total_weight = 0
        for node in self.nodes:
            total_weight += self.weights.get(node, 1)

        for node in self.nodes:
            weight = 1

            if node in self.weights:
                weight = self.weights.get(node)

            factor = math.floor((40 * len(self.nodes) * weight) / total_weight)

            for j in range(0, int(factor)):
                b_key = bytearray(self._hash_digest('%s-%s' % (node, j)))

                for i in range(0, 3):
                    key = self._hash_val(b_key, lambda x: x + i * 4)
                    self.ring[key] = node
                    self._sorted_keys.append(key)

        self._sorted_keys.sort()