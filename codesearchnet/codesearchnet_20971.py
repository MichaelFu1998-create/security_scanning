def set_data(self, data={}, datetime_fields=[]):
        """ Set entity data

        Args:
            data (dict): Entity data
            datetime_fields (array): Fields that should be parsed as datetimes
        """
        if datetime_fields:
            for field in datetime_fields:
                if field in data:
                    data[field] = self._parse_datetime(data[field])

        super(CampfireEntity, self).set_data(data)