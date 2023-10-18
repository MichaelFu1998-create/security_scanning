def format(self, record):
        """formats a logging.Record into a standard json log entry

        :param record: record to be formatted
        :type record: logging.Record
        :return: the formatted json string
        :rtype: string
        """

        record_fields = record.__dict__.copy()
        self._set_exc_info(record_fields)

        event_name = 'default'
        if record_fields.get('event_name'):
            event_name = record_fields.pop('event_name')

        log_level = 'INFO'
        if record_fields.get('log_level'):
            log_level = record_fields.pop('log_level')

        [record_fields.pop(k) for k in record_fields.keys()
         if k not in self.fields]

        defaults = self.defaults.copy()
        fields = self.fields.copy()
        fields.update(record_fields)
        filtered_fields = {}
        for k, v in fields.iteritems():
            if v is not None:
                filtered_fields[k] = v

        defaults.update({
            'event_timestamp': self._get_now(),
            'event_name': event_name,
            'log_level': log_level,
            'fields': filtered_fields})

        return json.dumps(defaults, default=self.json_default)