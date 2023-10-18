def p_prj_uri_art_3(self, p):
        """prj_uri_art : ART_PRJ_URI error"""
        self.error = True
        msg = ERROR_MESSAGES['ART_PRJ_URI_VALUE'].format(p.lineno(1))
        self.logger.log(msg)