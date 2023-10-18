def set_created_date(self, doc, created):
        """Sets created date, Raises CardinalityError if
        created date already set.
        Raises SPDXValueError if created is not a date.
        """
        if not self.created_date_set:
            self.created_date_set = True
            date = utils.datetime_from_iso_format(created)
            if date is not None:
                doc.creation_info.created = date
                return True
            else:
                raise SPDXValueError('CreationInfo::Date')
        else:
            raise CardinalityError('CreationInfo::Created')