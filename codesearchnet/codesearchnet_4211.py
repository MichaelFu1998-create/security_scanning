def p_annotation_date_1(self, p):
        """annotation_date : ANNOTATION_DATE DATE"""
        try:
            if six.PY2:
                value = p[2].decode(encoding='utf-8')
            else:
                value = p[2]
            self.builder.add_annotation_date(self.document, value)
        except CardinalityError:
            self.more_than_one_error('AnnotationDate', p.lineno(1))
        except OrderError:
            self.order_error('AnnotationDate', 'Annotator', p.lineno(1))