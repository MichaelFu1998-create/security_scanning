def package_for_editor_signavio(self, spec, filename):
        """
        Adds the SVG files to the archive for this BPMN file.
        """
        signavio_file = filename[:-len('.bpmn20.xml')] + '.signavio.xml'
        if os.path.exists(signavio_file):
            self.write_file_to_package_zip(
                "src/" + self._get_zip_path(signavio_file), signavio_file)

            f = open(signavio_file, 'r')
            try:
                signavio_tree = ET.parse(f)
            finally:
                f.close()
            svg_node = one(signavio_tree.findall('.//svg-representation'))
            self.write_to_package_zip("%s.svg" % spec.name, svg_node.text)