def set_doc_version(self, doc, value):
        """
        Set the document version.
        Raise SPDXValueError if malformed value, CardinalityError
        if already defined
        """
        if not self.doc_version_set:
            self.doc_version_set = True
            m = self.VERS_STR_REGEX.match(value)
            if m is None:
                raise SPDXValueError('Document::Version')
            else:
                doc.version = version.Version(major=int(m.group(1)),
                                              minor=int(m.group(2)))
                return True
        else:
            raise CardinalityError('Document::Version')