def p_annotation_type_1(self, p):
        """annotation_type : ANNOTATION_TYPE LINE"""
        try:
            if six.PY2:
                value = p[2].decode(encoding='utf-8')
            else:
                value = p[2]
            self.builder.add_annotation_type(self.document, value)
        except CardinalityError:
            self.more_than_one_error('AnnotationType', p.lineno(1))
        except SPDXValueError:
            self.error = True
            msg = ERROR_MESSAGES['ANNOTATION_TYPE_VALUE'].format(p.lineno(1))
            self.logger.log(msg)
        except OrderError:
            self.order_error('AnnotationType', 'Annotator', p.lineno(1))