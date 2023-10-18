def create_package(self):
        """
        Creates the package, writing the data out to the provided file-like
        object.
        """

        # Check that all files exist (and calculate the longest shared path
        # prefix):
        self.input_path_prefix = None
        for filename in self.input_files:
            if not os.path.isfile(filename):
                raise ValueError(
                    '%s does not exist or is not a file' % filename)
            if self.input_path_prefix:
                full = os.path.abspath(os.path.dirname(filename))
                while not (full.startswith(self.input_path_prefix) and
                           self.input_path_prefix):
                    self.input_path_prefix = self.input_path_prefix[:-1]
            else:
                self.input_path_prefix = os.path.abspath(
                    os.path.dirname(filename))

        # Parse all of the XML:
        self.bpmn = {}
        for filename in self.input_files:
            bpmn = ET.parse(filename)
            self.bpmn[os.path.abspath(filename)] = bpmn

        # Now run through pre-parsing and validation:
        for filename, bpmn in list(self.bpmn.items()):
            bpmn = self.pre_parse_and_validate(bpmn, filename)
            self.bpmn[os.path.abspath(filename)] = bpmn

        # Now check that we can parse it fine:
        for filename, bpmn in list(self.bpmn.items()):
            self.parser.add_bpmn_xml(bpmn, filename=filename)

        self.wf_spec = self.parser.get_spec(self.entry_point_process)

        # Now package everything:
        self.package_zip = zipfile.ZipFile(
            self.package_file, "w", compression=zipfile.ZIP_DEFLATED)

        done_files = set()
        for spec in self.wf_spec.get_specs_depth_first():
            filename = spec.file
            if filename not in done_files:
                done_files.add(filename)

                bpmn = self.bpmn[os.path.abspath(filename)]
                self.write_to_package_zip(
                    "%s.bpmn" % spec.name, ET.tostring(bpmn.getroot()))

                self.write_file_to_package_zip(
                    "src/" + self._get_zip_path(filename), filename)

                self._call_editor_hook('package_for_editor', spec, filename)

        self.write_meta_data()
        self.write_manifest()

        self.package_zip.close()