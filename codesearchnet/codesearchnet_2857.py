def setup(self, context):
    """Implements TextFile Generator's setup method"""
    myindex = context.get_partition_index()
    self._files_to_consume = self._files[myindex::context.get_num_partitions()]
    self.logger.info("TextFileSpout files to consume %s" % self._files_to_consume)
    self._lines_to_consume = self._get_next_lines()
    self._emit_count = 0