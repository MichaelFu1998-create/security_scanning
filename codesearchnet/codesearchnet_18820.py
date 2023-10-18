def _clean_xml(self, path_to_xml):
        """Clean MARCXML harvested from OAI.

        Allows the xml to be used with BibUpload or BibRecord.

        :param xml: either XML as a string or path to an XML file

        :return: ElementTree of clean data
        """
        try:
            if os.path.isfile(path_to_xml):
                tree = ET.parse(path_to_xml)
                root = tree.getroot()
            else:
                root = ET.fromstring(path_to_xml)
        except Exception, e:
            self.logger.error("Could not read OAI XML, aborting filter!")
            raise e
        strip_xml_namespace(root)
        return root