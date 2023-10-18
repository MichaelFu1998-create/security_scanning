def _normalize_article_dir_with_dtd(self, path):
        """
        main.xml from Elsevier assume the existence of a local DTD.
        This procedure install the DTDs next to the main.xml file
        and normalize it using xmllint in order to resolve all namespaces
        and references.
        """
        if exists(join(path, 'resolved_main.xml')):
            return
        main_xml_content = open(join(path, 'main.xml')).read()
        arts = ['art501.dtd','art510.dtd','art520.dtd','art540.dtd']
        tmp_extracted = 0
        for art in arts:
            if art in main_xml_content:
                self._extract_correct_dtd_package(art.split('.')[0], path)
                tmp_extracted = 1

        if not tmp_extracted:
            message = "It looks like the path " + path
            message += "does not contain an art501, art510, art520 or art540 in main.xml file"
            self.logger.error(message)
            raise ValueError(message)
        command = ["xmllint", "--format", "--loaddtd",
                   join(path, 'main.xml'),
                   "--output", join(path, 'resolved_main.xml')]
        dummy, dummy, cmd_err = run_shell_command(command)
        if cmd_err:
            message = "Error in cleaning %s: %s" % (
                join(path, 'main.xml'), cmd_err)
            self.logger.error(message)
            raise ValueError(message)