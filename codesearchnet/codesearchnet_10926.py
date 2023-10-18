def get_timestamps_part(self, name):
        """Return matching (timestamps, particles) pytables arrays.
        """
        par_name = name + '_par'
        timestamps = self.ts_store.h5file.get_node('/timestamps', name)
        particles = self.ts_store.h5file.get_node('/timestamps', par_name)
        return timestamps, particles