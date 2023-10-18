def set_spdx_doc_uri(self, doc, spdx_doc_uri):
        """
        Sets the `spdx_document_uri` attribute of the `ExternalDocumentRef`
        object.
        """
        if validations.validate_doc_namespace(spdx_doc_uri):
            doc.ext_document_references[-1].spdx_document_uri = spdx_doc_uri
        else:
            raise SPDXValueError('Document::ExternalDocumentRef')