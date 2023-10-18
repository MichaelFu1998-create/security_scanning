def _crawl_elsevier_and_find_issue_xml(self):
        """
        Information about the current volume, issue, etc. is available
        in a file called issue.xml that is available in a higher directory.
        """
        self._found_issues = []
        if not self.path and not self.package_name:
            for issue in self.conn._get_issues():
                dirname = issue.rstrip('/issue.xml')
                try:
                    self._normalize_issue_dir_with_dtd(dirname)
                    self._found_issues.append(dirname)
                except Exception as err:
                    register_exception()
                    print("ERROR: can't normalize %s: %s" % (dirname, err))
        else:
            def visit(dummy, dirname, names):
                if "issue.xml" in names:
                    try:
                        self._normalize_issue_dir_with_dtd(dirname)
                        self._found_issues.append(dirname)
                    except Exception as err:
                        register_exception()
                        print("ERROR: can't normalize %s: %s"
                              % (dirname, err))
            walk(self.path, visit, None)