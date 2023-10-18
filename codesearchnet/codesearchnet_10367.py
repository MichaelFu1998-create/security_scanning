def _get_gmx_docs(self):
        """Extract standard gromacs doc

        Extract by running the program and chopping the header to keep from
        'DESCRIPTION' onwards.
        """
        if self._doc_cache is not None:
            return self._doc_cache

        try:
            logging.disable(logging.CRITICAL)
            rc, header, docs = self.run('h', stdout=PIPE, stderr=PIPE, use_input=False)
        except:
            logging.critical("Invoking command {0} failed when determining its doc string. Proceed with caution".format(self.command_name))
            self._doc_cache = "(No Gromacs documentation available)"
            return self._doc_cache
        finally:
            # ALWAYS restore logging...
            logging.disable(logging.NOTSET)

        # The header is on STDOUT and is ignored. The docs are read from STDERR in GMX 4.
        m = re.match(self.doc_pattern, docs, re.DOTALL)

        if m is None:
            # In GMX 5, the opposite is true (Grrr)
            m = re.match(self.doc_pattern, header, re.DOTALL)
            if m is None:
                self._doc_cache = "(No Gromacs documentation available)"
                return self._doc_cache

        self._doc_cache = m.group('DOCS')
        return self._doc_cache