def set_doc_data_lic(self, doc, res):
        """
        Set the document data license.
        Raise exceptions:
        - SPDXValueError if malformed value,
        - CardinalityError if already defined.
        """
        if not self.doc_data_lics_set:
            self.doc_data_lics_set = True
            # TODO: what is this split?
            res_parts = res.split('/')
            if len(res_parts) != 0:
                identifier = res_parts[-1]
                doc.data_license = document.License.from_identifier(identifier)
            else:
                raise SPDXValueError('Document::License')
        else:
            raise CardinalityError('Document::License')