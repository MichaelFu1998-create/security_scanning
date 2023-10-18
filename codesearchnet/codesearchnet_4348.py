def p_file_chk_sum(self, f_term, predicate):
        """Sets file checksum. Assumes SHA1 algorithm without checking."""
        try:
            for _s, _p, checksum in self.graph.triples((f_term, predicate, None)):
                for _, _, value in self.graph.triples((checksum, self.spdx_namespace['checksumValue'], None)):
                    self.builder.set_file_chksum(self.doc, six.text_type(value))
        except CardinalityError:
            self.more_than_one_error('File checksum')