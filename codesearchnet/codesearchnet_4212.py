def p_annotation_comment_1(self, p):
        """annotation_comment : ANNOTATION_COMMENT TEXT"""
        try:
            if six.PY2:
                value = p[2].decode(encoding='utf-8')
            else:
                value = p[2]
            self.builder.add_annotation_comment(self.document, value)
        except CardinalityError:
            self.more_than_one_error('AnnotationComment', p.lineno(1))
        except OrderError:
            self.order_error('AnnotationComment', 'Annotator', p.lineno(1))