def readObject(self):
    """read object"""
    try:
      _, res = self._read_and_exec_opcode(ident=0)

      position_bak = self.object_stream.tell()
      the_rest = self.object_stream.read()
      if len(the_rest):
        log_error("Warning!!!!: Stream still has %s bytes left.\
Enable debug mode of logging to see the hexdump." % len(the_rest))
        log_debug(self._create_hexdump(the_rest))
      else:
        log_debug("Java Object unmarshalled succesfully!")
      self.object_stream.seek(position_bak)

      return res
    except Exception:
      self._oops_dump_state()
      raise