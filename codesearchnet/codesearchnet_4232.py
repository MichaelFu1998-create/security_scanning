def set_doc_name(self, doc, name):
        """Sets the document name.
        Raises CardinalityError if already defined.
        """
        if not self.doc_name_set:
            doc.name = name
            self.doc_name_set = True
            return True
        else:
            raise CardinalityError('Document::Name')