def get_record(self, record):
        """ Reads a dom xml element in oaidc format and
            returns the bibrecord object """
        self.document = record
        rec = create_record()
        language = self._get_language()
        if language and language != 'en':
            record_add_field(rec, '041', subfields=[('a', language)])
        publisher = self._get_publisher()
        date = self._get_date()
        if publisher and date:
            record_add_field(rec, '260', subfields=[('b', publisher),
                                                    ('c', date)])
        elif publisher:
            record_add_field(rec, '260', subfields=[('b', publisher)])
        elif date:
            record_add_field(rec, '260', subfields=[('c', date)])
        title = self._get_title()
        if title:
            record_add_field(rec, '245', subfields=[('a', title)])
        record_copyright = self._get_copyright()
        if record_copyright:
            record_add_field(rec, '540', subfields=[('a', record_copyright)])
        subject = self._get_subject()
        if subject:
            record_add_field(rec, '650', ind1='1', ind2='7', subfields=[('a', subject),
                                                                        ('2', 'PoS')])
        authors = self._get_authors()
        first_author = True
        for author in authors:
            subfields = [('a', author[0])]
            for affiliation in author[1]:
                subfields.append(('v', affiliation))
            if first_author:
                record_add_field(rec, '100', subfields=subfields)
                first_author = False
            else:
                record_add_field(rec, '700', subfields=subfields)
        identifier = self.get_identifier()
        conference = identifier.split(':')[2]
        conference = conference.split('/')[0]
        contribution = identifier.split(':')[2]
        contribution = contribution.split('/')[1]
        record_add_field(rec, '773', subfields=[('p', 'PoS'),
                                                ('v', conference.replace(' ', '')),
                                                ('c', contribution),
                                                ('y', date[:4])])
        record_add_field(rec, '980', subfields=[('a', 'ConferencePaper')])
        record_add_field(rec, '980', subfields=[('a', 'HEP')])
        return rec