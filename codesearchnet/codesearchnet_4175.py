def p_prj_home_art_1(self, p):
        """prj_home_art : ART_PRJ_HOME LINE"""
        try:
            self.builder.set_file_atrificat_of_project(self.document, 'home', p[2])
        except OrderError:
            self.order_error('ArtificatOfProjectHomePage', 'FileName', p.lineno(1))