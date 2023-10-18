def _normalize_issue_dir_with_dtd(self, path):
        """
        issue.xml from Elsevier assume the existence of a local DTD.
        This procedure install the DTDs next to the issue.xml file
        and normalize it using xmllint in order to resolve all namespaces
        and references.
        """
        if exists(join(path, 'resolved_issue.xml')):
            return
        issue_xml_content = open(join(path, 'issue.xml')).read()
        sis = ['si510.dtd', 'si520.dtd', 'si540.dtd']
        tmp_extracted = 0
        for si in sis:
            if si in issue_xml_content:
                self._extract_correct_dtd_package(si.split('.')[0], path)
                tmp_extracted = 1

        if not tmp_extracted:
            message = "It looks like the path " + path
            message += " does not contain an si510, si520 or si540 in issue.xml file"
            self.logger.error(message)
            raise ValueError(message)
        command = ["xmllint", "--format", "--loaddtd",
                   join(path, 'issue.xml'),
                   "--output", join(path, 'resolved_issue.xml')]
        dummy, dummy, cmd_err = run_shell_command(command)
        if cmd_err:
            message = "Error in cleaning %s: %s" % (
                join(path, 'issue.xml'), cmd_err)
            self.logger.error(message)
            raise ValueError(message)