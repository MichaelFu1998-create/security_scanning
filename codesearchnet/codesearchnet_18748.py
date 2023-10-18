def get_record(self, fileName, ref_extract_callback=None):
        """
        Gets the Marc xml of the files in xaml_jp directory

        :param fileName: the name of the file to parse.
        :type fileName: string
        :param refextract_callback: callback to be used to extract
                                    unstructured references. It should
                                    return a marcxml formated string
                                    of the reference.
        :type refextract_callback: callable

        :returns: a string with the marc xml version of the file.
        """
        self.document = parse(fileName)
        article_type = self._get_article_type()
        if article_type not in ['research-article',
                                'introduction',
                                'letter']:
            return ''
        rec = create_record()
        title, subtitle, notes = self._get_title()
        subfields = []
        if subtitle:
            subfields.append(('b', subtitle))
        if title:
            subfields.append(('a', title))
            record_add_field(rec, '245', subfields=subfields)
        subjects = self.document.getElementsByTagName('kwd')
        subjects = map(xml_to_text, subjects)
        for note_id in notes:
            note = self._get_note(note_id)
            if note:
                record_add_field(rec, '500', subfields=[('a', note)])
        for subject in subjects:
            record_add_field(rec, '650', ind1='1', ind2='7',
                             subfields=[('2', 'EDPSciences'),
                                        ('a', subject)])
        keywords = self._get_keywords()
        for keyword in keywords:
            record_add_field(rec, '653', ind1='1', subfields=[('a', keyword),
                                                              ('9', 'author')])
        journal, volume, issue, year, date, doi, page,\
            fpage, lpage = self._get_publication_information()
        astronomy_journals = ['EAS Publ.Ser.', 'Astron.Astrophys.']
        if journal in astronomy_journals:
            record_add_field(rec, '650', ind1='1', ind2='7',
                             subfields=[('2', 'INSPIRE'),
                                        ('a', 'Astrophysics')])
        if date:
            record_add_field(rec, '260', subfields=[('c', date),
                                                    ('t', 'published')])
        if doi:
            record_add_field(rec, '024', ind1='7', subfields=[('a', doi),
                                                              ('2', 'DOI')])
        abstract = self._get_abstract()
        abstract = self._format_abstract(abstract)
        if abstract:
            record_add_field(rec, '520', subfields=[('a', abstract),
                                                    ('9', 'EDPSciences')])
        license, license_type, license_url = self._get_license()
        subfields = []
        if license:
            subfields.append(('a', license))
        if license_url:
            subfields.append(('u', license_url))
        if subfields:
            record_add_field(rec, '540', subfields=subfields)
        if license_type == 'open-access':
            self._attach_fulltext(rec, doi)
        number_of_pages = self._get_page_count()
        if number_of_pages:
            record_add_field(rec, '300', subfields=[('a', number_of_pages)])
        c_holder, c_year, c_statement = self._get_copyright()
        if c_holder and c_year:
            record_add_field(rec, '542', subfields=[('d', c_holder),
                                                    ('g', c_year),
                                                    ('e', 'Article')])
        elif c_statement:
            record_add_field(rec, '542', subfields=[('f', c_statement),
                                                    ('e', 'Article')])
        subfields = []
        if journal:
            subfields.append(('p', journal))
        if issue:
            subfields.append(('n', issue))
        if volume:
            subfields.append(('v', volume))
        if fpage and lpage:
            subfields.append(('c', '%s-%s' % (fpage,
                                              lpage)))
        elif page:
            subfields.append(('c', page))
        if year:
            subfields.append(('y', year))
        record_add_field(rec, '773', subfields=subfields)
        record_add_field(rec, '980', subfields=[('a', 'HEP')])
        conference = ''
        for tag in self.document.getElementsByTagName('conference'):
            conference = xml_to_text(tag)
        if conference:
            record_add_field(rec, '980', subfields=[('a', 'ConferencePaper')])
            record_add_field(rec, '500', subfields=[('a', conference)])
        self._add_references(rec, ref_extract_callback)
        self._add_authors(rec)
        try:
            return record_xml_output(rec)
        except UnicodeDecodeError:
            message = "Found a bad char in the file for the article " + doi
            sys.stderr.write(message)
            return ""