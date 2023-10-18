def dict_to_row(cls, observation_data):
        """
        Takes a dictionary of observation data and converts it to a list
        of fields according to AAVSO visual format specification.

        :param cls: current class
        :param observation_data: a single observation as a dictionary
        """
        row = []
        row.append(observation_data['name'])
        row.append(observation_data['date'])
        row.append(observation_data['magnitude'])
        comment_code = observation_data.get('comment_code', 'na')
        if not comment_code:
            comment_code = 'na'
        row.append(comment_code)
        comp1 = observation_data.get('comp1', 'na')
        if not comp1:
            comp1 = 'na'
        row.append(comp1)
        comp2 = observation_data.get('comp2', 'na')
        if not comp2:
            comp2 = 'na'
        row.append(comp2)
        chart = observation_data.get('chart', 'na')
        if not chart:
            chart = 'na'
        row.append(chart)
        notes = observation_data.get('notes', 'na')
        if not notes:
            notes = 'na'
        row.append(notes)
        return row