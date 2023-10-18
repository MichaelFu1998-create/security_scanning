def conference_record_stop(self, call_params):
        """REST Conference RecordStop
        """
        path = '/' + self.api_version + '/ConferenceRecordStop/'
        method = 'POST'
        return self.request(path, method, call_params)