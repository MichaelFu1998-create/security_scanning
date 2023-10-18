def row_to_dict(cls, row):
        """
        Converts a raw input record to a dictionary of observation data.

        :param cls: current class
        :param row: a single observation as a list or tuple
        """
        comment_code = row[3]
        if comment_code.lower() == 'na':
            comment_code = ''
        comp1 = row[4]
        if comp1.lower() == 'na':
            comp1 = ''
        comp2 = row[5]
        if comp2.lower() == 'na':
            comp2 = ''
        chart = row[6]
        if chart.lower() == 'na':
            chart = ''
        notes = row[7]
        if notes.lower() == 'na':
            notes = ''
        return {
            'name': row[0],
            'date': row[1],
            'magnitude': row[2],
            'comment_code': comment_code,
            'comp1': comp1,
            'comp2': comp2,
            'chart': chart,
            'notes': notes,
        }