def handle_pkg_optional_fields(self, package, package_node):
        """
        Write package optional fields.
        """
        self.handle_package_literal_optional(package, package_node, self.spdx_namespace.versionInfo, 'version')
        self.handle_package_literal_optional(package, package_node, self.spdx_namespace.packageFileName, 'file_name')
        self.handle_package_literal_optional(package, package_node, self.spdx_namespace.supplier, 'supplier')
        self.handle_package_literal_optional(package, package_node, self.spdx_namespace.originator, 'originator')
        self.handle_package_literal_optional(package, package_node, self.spdx_namespace.sourceInfo, 'source_info')
        self.handle_package_literal_optional(package, package_node, self.spdx_namespace.licenseComments, 'license_comment')
        self.handle_package_literal_optional(package, package_node, self.spdx_namespace.summary, 'summary')
        self.handle_package_literal_optional(package, package_node, self.spdx_namespace.description, 'description')

        if package.has_optional_field('check_sum'):
            checksum_node = self.create_checksum_node(package.check_sum)
            self.graph.add((package_node, self.spdx_namespace.checksum, checksum_node))

        if package.has_optional_field('homepage'):
            homepage_node = URIRef(self.to_special_value(package.homepage))
            homepage_triple = (package_node, self.doap_namespace.homepage, homepage_node)
            self.graph.add(homepage_triple)