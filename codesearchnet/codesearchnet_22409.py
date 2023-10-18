def prepare(self, input_files, bundle):
        """
        :type input_files: list[static_bundle.files.StaticFileResult]
        :type bundle: static_bundle.bundles.AbstractBundle
        :rtype: list
        """
        out = []
        for input_file in input_files:
            if input_file.extension == "less" and os.path.isfile(input_file.abs_path):
                output_file = self.get_compile_file(input_file, bundle)
                self.compile(input_file, output_file)
                out.append(output_file)
            else:
                out.append(input_file)
        return out