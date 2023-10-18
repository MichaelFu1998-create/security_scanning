def p_review_date_1(self, p):
        """review_date : REVIEW_DATE DATE"""
        try:
            if six.PY2:
                value = p[2].decode(encoding='utf-8')
            else:
                value = p[2]
            self.builder.add_review_date(self.document, value)
        except CardinalityError:
            self.more_than_one_error('ReviewDate', p.lineno(1))
        except OrderError:
            self.order_error('ReviewDate', 'Reviewer', p.lineno(1))