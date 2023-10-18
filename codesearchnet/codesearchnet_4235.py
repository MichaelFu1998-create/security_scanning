def set_doc_namespace(self, doc, namespace):
        """Sets the document namespace.
        Raise SPDXValueError if malformed value, CardinalityError
        if already defined.
        """
        if not self.doc_namespace_set:
            self.doc_namespace_set = True
            if validations.validate_doc_namespace(namespace):
                doc.namespace = namespace
                return True
            else:
                raise SPDXValueError('Document::Namespace')
        else:
            raise CardinalityError('Document::Comment')