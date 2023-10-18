def flush_buffer(self):
        """flush all buffered string into code"""
        self.code_builder.add_line('{0}.extend([{1}])',
                                   self.result_var, ','.join(self.buffered))
        self.buffered = []