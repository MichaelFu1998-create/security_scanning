def _crawl_springer_and_find_main_xml(self):
        """
        A package contains several subdirectory corresponding to each article.
        An article is actually identified by the existence of a main.pdf and
        a main.xml in a given directory.
        """
        self.found_articles = []

        def visit(arg, dirname, names):
            files = [filename for filename in names if "nlm.xml" in filename]
            if not files:
                files = [filename for filename in names
                         if ".xml.scoap" in filename]
            if files:
                try:
                    # self._normalize_article_dir_with_dtd(dirname)
                    self.found_articles.append(dirname)
                except Exception as err:
                    register_exception()
                    print "ERROR: can't normalize %s: %s" % (dirname, err)

        if hasattr(self, 'path_unpacked'):
            for path in self.path_unpacked:
                walk(path, visit, None)
        elif self.path:
            walk(self.path, visit, None)
        else:
            self.logger.info("Nothing to do.")