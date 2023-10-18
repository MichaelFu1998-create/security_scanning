def _generate_character_map(self):
        """Generate character translation map (latin1 pos to texture pos)"""
        self._ct = [-1] * 256
        index = 0
        for crange in self._meta.character_ranges:
            for cpos in range(crange['min'], crange['max'] + 1):
                self._ct[cpos] = index
                index += 1