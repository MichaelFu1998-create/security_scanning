def p_creator_comment_1(self, p):
        """creator_comment : CREATOR_COMMENT TEXT"""
        try:
            if six.PY2:
                value = p[2].decode(encoding='utf-8')
            else:
                value = p[2]
            self.builder.set_creation_comment(self.document, value)
        except CardinalityError:
            self.more_than_one_error('CreatorComment', p.lineno(1))