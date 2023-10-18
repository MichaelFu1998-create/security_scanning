def get_source_for(self, asm_offset, runtime=True):
        """ Solidity source code snippet related to `asm_pos` evm bytecode offset.
            If runtime is False, initialization bytecode source map is used
        """
        srcmap = self.get_srcmap(runtime)

        try:
            beg, size, _, _ = srcmap[asm_offset]
        except KeyError:
            #asm_offset pointing outside the known bytecode
            return ''

        output = ''
        nl = self.source_code[:beg].count('\n') + 1
        snippet = self.source_code[beg:beg + size]
        for l in snippet.split('\n'):
            output += '    %s  %s\n' % (nl, l)
            nl += 1
        return output