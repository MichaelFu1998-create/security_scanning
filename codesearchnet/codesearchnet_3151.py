def _import_concrete_memory(self, from_addr, to_addr):
        """
        for each address in this range need to read from concrete and write to symbolic
        it's possible that there will be invalid/unmapped addresses in this range. need to skip to next map if so
        also need to mark all of these addresses as now in the symbolic store

        :param int from_addr:
        :param int to_addr:
        :return:
        """
        logger.debug("Importing concrete memory: {:x} - {:x} ({} bytes)".format(from_addr, to_addr, to_addr - from_addr))

        for m in self.maps:
            span = interval_intersection(m.start, m.end, from_addr, to_addr)
            if span is None:
                continue

            start, stop = span

            for addr in range(start, stop):
                if addr in self.backed_by_symbolic_store:
                    continue

                self.backing_array[addr] = Memory.read(self, addr, 1)[0]
                self.backed_by_symbolic_store.add(addr)