def p_prj_name_art_1(self, p):
        """prj_name_art : ART_PRJ_NAME LINE"""
        try:
            if six.PY2:
                value = p[2].decode(encoding='utf-8')
            else:
                value = p[2]
            self.builder.set_file_atrificat_of_project(self.document, 'name', value)
        except OrderError:
            self.order_error('ArtifactOfProjectName', 'FileName', p.lineno(1))