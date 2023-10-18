def t_mediaquery_t_semicolon(self, t):
        r';'
        # This can happen only as part of a CSS import statement. The
        # "mediaquery" state is reused there. Ordinary media queries always
        # end at '{', i.e. when a block is opened.
        t.lexer.pop_state()  # state mediaquery
        # We have to pop the 'import' state here because we already ate the
        # t_semicolon and won't trigger t_import_t_semicolon.
        t.lexer.pop_state()  # state import
        return t