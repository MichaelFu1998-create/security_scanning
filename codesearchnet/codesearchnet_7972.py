def fetch(self, range_start, range_end):
        """
        Fetches speeches from the ListarDiscursosPlenario endpoint of the
        SessoesReunioes (SessionsReunions) API.

        The date range provided should be specified as a string using the
        format supported by the API (%d/%m/%Y)
        """
        range_dates = {'dataIni': range_start, 'dataFim': range_end}
        url = self.URL.format(**range_dates)
        xml = urllib.request.urlopen(url)

        tree = ET.ElementTree(file=xml)
        records = self._parse_speeches(tree.getroot())

        return pd.DataFrame(records, columns=[
            'session_code',
            'session_date',
            'session_num',
            'phase_code',
            'phase_desc',
            'speech_speaker_num',
            'speech_speaker_name',
            'speech_speaker_party',
            'speech_speaker_state',
            'speech_started_at',
            'speech_room_num',
            'speech_insertion_num'
        ])