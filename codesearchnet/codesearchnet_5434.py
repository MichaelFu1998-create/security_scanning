def write_meta_data(self):
        """
        Writes the metadata.ini file to the archive.
        """
        config = configparser.ConfigParser()

        config.add_section('MetaData')
        config.set('MetaData', 'entry_point_process', self.wf_spec.name)
        if self.editor:
            config.set('MetaData', 'editor', self.editor)

        for k, v in self.meta_data:
            config.set('MetaData', k, v)

        if not self.PARSER_CLASS == BpmnParser:
            config.set('MetaData', 'parser_class_module',
                       inspect.getmodule(self.PARSER_CLASS).__name__)
            config.set('MetaData', 'parser_class', self.PARSER_CLASS.__name__)

        ini = StringIO()
        config.write(ini)
        self.write_to_package_zip(self.METADATA_FILE, ini.getvalue())