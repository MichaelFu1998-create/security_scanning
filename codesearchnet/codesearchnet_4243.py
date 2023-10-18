def set_creation_comment(self, doc, comment):
        """Sets creation comment, Raises CardinalityError if
        comment already set.
        Raises SPDXValueError if not free form text.
        """
        if not self.creation_comment_set:
            self.creation_comment_set = True
            if validations.validate_creation_comment(comment):
                doc.creation_info.comment = str_from_text(comment)
                return True
            else:
                raise SPDXValueError('CreationInfo::Comment')
        else:
            raise CardinalityError('CreationInfo::Comment')