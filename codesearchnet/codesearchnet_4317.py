def create_package_node(self, package):
        """
        Return a Node representing the package.
        Files must have been added to the graph before this method is called.
        """
        package_node = BNode()
        type_triple = (package_node, RDF.type, self.spdx_namespace.Package)
        self.graph.add(type_triple)
        # Handle optional fields:
        self.handle_pkg_optional_fields(package, package_node)
        # package name
        name_triple = (package_node, self.spdx_namespace.name, Literal(package.name))
        self.graph.add(name_triple)
        # Package download location
        down_loc_node = (package_node, self.spdx_namespace.downloadLocation, self.to_special_value(package.download_location))
        self.graph.add(down_loc_node)
        # Handle package verification
        verif_node = self.package_verif_node(package)
        verif_triple = (package_node, self.spdx_namespace.packageVerificationCode, verif_node)
        self.graph.add(verif_triple)
        # Handle concluded license
        conc_lic_node = self.license_or_special(package.conc_lics)
        conc_lic_triple = (package_node, self.spdx_namespace.licenseConcluded, conc_lic_node)
        self.graph.add(conc_lic_triple)
        # Handle declared license
        decl_lic_node = self.license_or_special(package.license_declared)
        decl_lic_triple = (package_node, self.spdx_namespace.licenseDeclared, decl_lic_node)
        self.graph.add(decl_lic_triple)
        # Package licenses from files
        licenses_from_files_nodes = map(lambda el: self.license_or_special(el), package.licenses_from_files)
        lic_from_files_predicate = self.spdx_namespace.licenseInfoFromFiles
        lic_from_files_triples = [(package_node, lic_from_files_predicate, node) for node in licenses_from_files_nodes]
        for triple in lic_from_files_triples:
            self.graph.add(triple)
        # Copyright Text
        cr_text_node = self.to_special_value(package.cr_text)
        cr_text_triple = (package_node, self.spdx_namespace.copyrightText, cr_text_node)
        self.graph.add(cr_text_triple)
        # Handle files
        self.handle_package_has_file(package, package_node)
        return package_node