def parse(self, path_to_xml=None):
        """Parse an XML document and clean any namespaces."""
        if not path_to_xml:
            if not self.path:
                self.logger.error("No path defined!")
                return
            path_to_xml = self.path
        root = self._clean_xml(path_to_xml)

        # See first of this XML is clean or OAI request
        if root.tag.lower() == 'collection':
            tree = ET.ElementTree(root)
            self.records = element_tree_collection_to_records(tree)
        elif root.tag.lower() == 'record':
            new_root = ET.Element('collection')
            new_root.append(root)
            tree = ET.ElementTree(new_root)
            self.records = element_tree_collection_to_records(tree)
        else:
            # We have an OAI request
            header_subs = get_request_subfields(root)
            records = root.find('ListRecords')
            if records is None:
                records = root.find('GetRecord')
            if records is None:
                raise ValueError("Cannot find ListRecords or GetRecord!")

            tree = ET.ElementTree(records)
            for record, is_deleted in element_tree_oai_records(tree, header_subs):
                if is_deleted:
                    # It was OAI deleted. Create special record
                    self.deleted_records.append(
                        self.create_deleted_record(record)
                    )
                else:
                    self.records.append(record)