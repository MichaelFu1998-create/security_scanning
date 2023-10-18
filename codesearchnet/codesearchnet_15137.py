def _connect_rows(self, connections):
        """Connect the parsed rows."""
        for connection in connections:
            from_row_id = self._to_id(connection[FROM][ID])
            from_row = self._id_cache[from_row_id]
            from_row_start_index = connection[FROM].get(START, DEFAULT_START)
            from_row_number_of_possible_meshes = \
                from_row.number_of_produced_meshes - from_row_start_index
            to_row_id = self._to_id(connection[TO][ID])
            to_row = self._id_cache[to_row_id]
            to_row_start_index = connection[TO].get(START, DEFAULT_START)
            to_row_number_of_possible_meshes = \
                to_row.number_of_consumed_meshes - to_row_start_index
            meshes = min(from_row_number_of_possible_meshes,
                         to_row_number_of_possible_meshes)
            # TODO: test all kinds of connections
            number_of_meshes = connection.get(MESHES, meshes)
            from_row_stop_index = from_row_start_index + number_of_meshes
            to_row_stop_index = to_row_start_index + number_of_meshes
            assert 0 <= from_row_start_index <= from_row_stop_index
            produced_meshes = from_row.produced_meshes[
                from_row_start_index:from_row_stop_index]
            assert 0 <= to_row_start_index <= to_row_stop_index
            consumed_meshes = to_row.consumed_meshes[
                to_row_start_index:to_row_stop_index]
            assert len(produced_meshes) == len(consumed_meshes)
            mesh_pairs = zip(produced_meshes, consumed_meshes)
            for produced_mesh, consumed_mesh in mesh_pairs:
                produced_mesh.connect_to(consumed_mesh)