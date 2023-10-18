def add_creator(self, doc, creator):
        """Adds a creator to the document's creation info.
        Returns true if creator is valid.
        Creator must be built by an EntityBuilder.
        Raises SPDXValueError if not a creator type.
        """
        if validations.validate_creator(creator):
            doc.creation_info.add_creator(creator)
            return True
        else:
            raise SPDXValueError('CreationInfo::Creator')