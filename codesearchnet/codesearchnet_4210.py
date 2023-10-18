def p_review_comment_1(self, p):
        """review_comment : REVIEW_COMMENT TEXT"""
        try:
            if six.PY2:
                value = p[2].decode(encoding='utf-8')
            else:
                value = p[2]
            self.builder.add_review_comment(self.document, value)
        except CardinalityError:
            self.more_than_one_error('ReviewComment', p.lineno(1))
        except OrderError:
            self.order_error('ReviewComment', 'Reviewer', p.lineno(1))