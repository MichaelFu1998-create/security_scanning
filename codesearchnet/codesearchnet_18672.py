def _crawl_oxford_and_find_main_xml(self):
        """
        A package contains several subdirectory corresponding to each article.
        An article is actually identified by the existence of a main.pdf and
        a main.xml in a given directory.
        """
        self.found_articles = []

        def visit(arg, dirname, names):
            files = [filename for filename in names if ".xml" in filename]
            if files:
                try:
                    for f in files:
                        self.found_articles.append(join(dirname, f))

                except Exception as err:
                    register_exception()
                    print("ERROR: can't normalize %s: %s" % (dirname, err),
                          file=sys.stderr)

        if hasattr(self, 'path_unpacked'):
            walk(self.path_unpacked, visit, None)
        elif self.path:
            walk(self.path, visit, None)
        else:
            self.logger.info("Nothing to do.")