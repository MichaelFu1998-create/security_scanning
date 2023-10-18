def p_file_type(self, f_term, predicate):
        """Sets file type."""
        try:
            for _, _, ftype in self.graph.triples((f_term, predicate, None)):
                try:
                    if ftype.endswith('binary'):
                        ftype = 'BINARY'
                    elif ftype.endswith('source'):
                        ftype = 'SOURCE'
                    elif ftype.endswith('other'):
                        ftype = 'OTHER'
                    elif ftype.endswith('archive'):
                        ftype = 'ARCHIVE'
                    self.builder.set_file_type(self.doc, ftype)
                except SPDXValueError:
                    self.value_error('FILE_TYPE', ftype)
        except CardinalityError:
            self.more_than_one_error('file type')