def p_annotation_spdx_id_1(self, p):
        """annotation_spdx_id : ANNOTATION_SPDX_ID LINE"""
        try:
            if six.PY2:
                value = p[2].decode(encoding='utf-8')
            else:
                value = p[2]
            self.builder.set_annotation_spdx_id(self.document, value)
        except CardinalityError:
            self.more_than_one_error('SPDXREF', p.lineno(1))
        except OrderError:
            self.order_error('SPDXREF', 'Annotator', p.lineno(1))