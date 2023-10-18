def deserialize_workflow_spec(self, s_state, filename=None):
        """
        :param s_state: a byte-string with the contents of the packaged
        workflow archive, or a file-like object.

        :param filename: the name of the package file.
        """
        if isinstance(s_state, (str, bytes)):
            s_state = BytesIO(s_state)

        package_zip = zipfile.ZipFile(
            s_state, "r", compression=zipfile.ZIP_DEFLATED)
        config = configparser.ConfigParser()
        ini_fp = TextIOWrapper(
            package_zip.open(Packager.METADATA_FILE), encoding="UTF-8")
        try:
            config.read_file(ini_fp)
        finally:
            ini_fp.close()

        parser_class = BpmnParser

        try:
            parser_class_module = config.get(
                'MetaData', 'parser_class_module', fallback=None)
        except TypeError:
            # unfortunately the fallback= does not exist on python 2
            parser_class_module = config.get(
                'MetaData', 'parser_class_module', None)

        if parser_class_module:
            mod = __import__(parser_class_module, fromlist=[
                             config.get('MetaData', 'parser_class')])
            parser_class = getattr(mod, config.get('MetaData', 'parser_class'))

        parser = parser_class()

        for info in package_zip.infolist():
            parts = os.path.split(info.filename)
            if (len(parts) == 2 and
                    not parts[0] and parts[1].lower().endswith('.bpmn')):
                # It is in the root of the ZIP and is a BPMN file
                try:
                    svg = package_zip.read(info.filename[:-5] + '.svg')
                except KeyError:
                    svg = None

                bpmn_fp = package_zip.open(info)
                try:
                    bpmn = ET.parse(bpmn_fp)
                finally:
                    bpmn_fp.close()

                parser.add_bpmn_xml(
                    bpmn, svg=svg,
                    filename='%s:%s' % (filename, info.filename))

        return parser.get_spec(config.get('MetaData', 'entry_point_process'))