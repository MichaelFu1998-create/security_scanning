def get_data(self, **kwargs):
        """
        Get the data for a specific device for a specific end date

        Keyword Arguments:
            limit - max 288
            end_date - is Epoch in milliseconds

        :return:
        """
        limit = int(kwargs.get('limit', 288))
        end_date = kwargs.get('end_date', False)

        if end_date and isinstance(end_date, datetime.datetime):
            end_date = self.convert_datetime(end_date)

        if self.mac_address is not None:
            service_address = 'devices/%s' % self.mac_address
            self.api_instance.log('SERVICE ADDRESS: %s' % service_address)

            data = dict(limit=limit)

            # If endDate is left blank (not passed in), the most recent results will be returned.
            if end_date:
                data.update({'endDate': end_date})

            self.api_instance.log('DATA:')
            self.api_instance.log(data)

            return self.api_instance.api_call(service_address, **data)