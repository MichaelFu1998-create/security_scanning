def _walk(self, fd):
        """Walk and dump (disasm) descriptor.
        """
        top = '.{}'.format(fd.package) if len(fd.package) > 0 else ''
        
        for e in fd.enum_type: self._dump_enum(e, top)
        for m in fd.message_type: self. _dump_message(m, top)