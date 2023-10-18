def set_annotation_spdx_id(self, doc, spdx_id):
        """Sets the annotation SPDX Identifier.
        Raises CardinalityError if already set. OrderError if no annotator
        defined before.
        """
        if len(doc.annotations) != 0:
            if not self.annotation_spdx_id_set:
                self.annotation_spdx_id_set = True
                doc.annotations[-1].spdx_id = spdx_id
                return True
            else:
                raise CardinalityError('Annotation::SPDXREF')
        else:
            raise OrderError('Annotation::SPDXREF')