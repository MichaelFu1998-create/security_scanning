def t_string(self, t):
        # Start of a string
        r'\"'
        # abs_start is the absolute start of the string. We use this at the end
        # to know how many new lines we've consumed
        t.lexer.abs_start = t.lexer.lexpos
        # rel_pos is the begining of the unconsumed part of the string. It will
        # get modified when consuming escaped characters
        t.lexer.rel_pos = t.lexer.lexpos
        # The value of the consumed part of the string
        t.lexer.string_value = u''
        t.lexer.begin('string')