def parse_package(self, p_term):
        """Parses package fields."""
        # Check there is a pacakge name
        if not (p_term, self.spdx_namespace['name'], None) in self.graph:
            self.error = True
            self.logger.log('Package must have a name.')
            # Create dummy package so that we may continue parsing the rest of
            # the package fields.
            self.builder.create_package(self.doc, 'dummy_package')
        else:
            for _s, _p, o in self.graph.triples((p_term, self.spdx_namespace['name'], None)):
                try:
                    self.builder.create_package(self.doc, six.text_type(o))
                except CardinalityError:
                    self.more_than_one_error('Package name')
                    break

        self.p_pkg_vinfo(p_term, self.spdx_namespace['versionInfo'])
        self.p_pkg_fname(p_term, self.spdx_namespace['packageFileName'])
        self.p_pkg_suppl(p_term, self.spdx_namespace['supplier'])
        self.p_pkg_originator(p_term, self.spdx_namespace['originator'])
        self.p_pkg_down_loc(p_term, self.spdx_namespace['downloadLocation'])
        self.p_pkg_homepg(p_term, self.doap_namespace['homepage'])
        self.p_pkg_chk_sum(p_term, self.spdx_namespace['checksum'])
        self.p_pkg_src_info(p_term, self.spdx_namespace['sourceInfo'])
        self.p_pkg_verif_code(p_term, self.spdx_namespace['packageVerificationCode'])
        self.p_pkg_lic_conc(p_term, self.spdx_namespace['licenseConcluded'])
        self.p_pkg_lic_decl(p_term, self.spdx_namespace['licenseDeclared'])
        self.p_pkg_lics_info_from_files(p_term, self.spdx_namespace['licenseInfoFromFiles'])
        self.p_pkg_comments_on_lics(p_term, self.spdx_namespace['licenseComments'])
        self.p_pkg_cr_text(p_term, self.spdx_namespace['copyrightText'])
        self.p_pkg_summary(p_term, self.spdx_namespace['summary'])
        self.p_pkg_descr(p_term, self.spdx_namespace['description'])