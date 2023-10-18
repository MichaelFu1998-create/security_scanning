def _normalize_article_dir_with_dtd(self, path):
        """
        TODO: main.xml from Springer assume the existence of a local DTD.
        This procedure install the DTDs next to the main.xml file
        and normalize it using xmllint in order to resolve all namespaces
        and references.
        """
        files = [filename for filename in listdir(path)
                 if "nlm.xml" in filename]
        if not files:
                files = [filename for filename in listdir(path)
                         if ".xml.scoap" in filename]
        if exists(join(path, 'resolved_main.xml')):
            return

        if 'JATS-archivearticle1.dtd' in open(join(path, files[0])).read():
            path_normalized = mkdtemp(prefix="scoap3_normalized_jats_",
                                      dir=CFG_TMPSHAREDDIR)
            ZipFile(CFG_SPRINGER_JATS_PATH).extractall(path_normalized)
        elif 'A++V2.4.dtd' in open(join(path, files[0])).read():
            path_normalized = mkdtemp(prefix="scoap3_normalized_app_",
                                      dir=CFG_TMPSHAREDDIR)
            ZipFile(CFG_SPRINGER_AV24_PATH).extractall(path_normalized)
        else:
            error_msg = ("It looks like the path %s does not contain an "
                         "JATS-archivearticle1.dtd nor A++V2.4.dtd XML file.")
            self.logger.error(error_msg % path)
            raise ValueError(error_msg % path)
        print "Normalizing %s" % (files[0],)
        (cmd_exit_code,
         cmd_out,
         cmd_err) = run_shell_command(("xmllint --format "
                                       "--loaddtd %s --output %s"),
                                      (join(path, files[0]),
                                       join(path_normalized,
                                            'resolved_main.xml')))
        if cmd_err:
            error_msg = "Error in cleaning %s: %s"
            self.logger.error(error_msg % (join(path, 'issue.xml'), cmd_err))
            raise ValueError(error_msg % (join(path, 'main.xml'), cmd_err))
        self.articles_normalized.append(path_normalized)