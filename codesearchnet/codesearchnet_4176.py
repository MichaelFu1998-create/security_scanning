def p_prj_home_art_2(self, p):
        """prj_home_art : ART_PRJ_HOME UN_KNOWN"""
        try:
            self.builder.set_file_atrificat_of_project(self.document,
                'home', utils.UnKnown())
        except OrderError:
            self.order_error('ArtifactOfProjectName', 'FileName', p.lineno(1))