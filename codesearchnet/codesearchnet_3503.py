def _interp_total_size(interp):
        """
        Compute total load size of interpreter.

        :param ELFFile interp: interpreter ELF .so
        :return: total load size of interpreter, not aligned
        :rtype: int
        """
        load_segs = [x for x in interp.iter_segments() if x.header.p_type == 'PT_LOAD']
        last = load_segs[-1]
        return last.header.p_vaddr + last.header.p_memsz