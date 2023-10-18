def get_record(self, filename, ref_extract_callback=None):
        """Get the MARCXML of the files in xaml_jp directory.

        :param filename: the name of the file to parse.
        :type filename: string
        :param refextract_callback: callback to be used to extract
                                    unstructured references. It should
                                    return a marcxml formated string
                                    of the reference.
        :type refextract_callback: callable

        :returns: a string with the marc xml version of the file.
        """
        self.document = parse(filename)

        article_type = self._get_article_type()
        if article_type not in ['research-article',
                                'corrected-article',
                                'original-article',
                                'introduction',
                                'letter',
                                'correction',
                                'addendum',
                                'review-article',
                                'rapid-communications']:
            return ""

        rec = create_record()
        title, subtitle, notes = self._get_title()
        subfields = []
        if subtitle:
            subfields.append(('b', subtitle))
        if title:
            title = fix_title_capitalization(title)
            subfields.append(('a', title))
            record_add_field(rec, '245', subfields=subfields)
        for note_id in notes:
            note = self._get_note(note_id)
            if note:
                record_add_field(rec, '500', subfields=[('a', note)])
        keywords = self._get_keywords()
        for keyword in keywords:
            record_add_field(rec, '653', ind1='1', subfields=[('a', keyword),
                                                              ('9', 'author')])
        journal, volume, issue, year, date, doi, page,\
            fpage, lpage = self._get_publication_information()
        if date:
            record_add_field(rec, '260', subfields=[('c', date),
                                                    ('t', 'published')])
        if doi:
            record_add_field(rec, '024', ind1='7', subfields=[('a', doi),
                                                              ('2', 'DOI')])
        abstract = self._get_abstract()
        if abstract:
            abstract = convert_html_subscripts_to_latex(abstract)
            record_add_field(rec, '520', subfields=[('a', abstract),
                                                    ('9', 'World Scientific')])
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
        if article_type == 'correction':
            subfields.append(('m', 'Erratum'))
        elif article_type == 'addendum':
            subfields.append(('m', 'Addendum'))
        record_add_field(rec, '773', subfields=subfields)

        collections = self.get_collection(journal)
        for collection in collections:
            record_add_field(rec, '980', subfields=[collection])

        self._add_authors(rec)
        if article_type in ['correction',
                            'addendum']:
            related_article = self._get_related_article()
            if related_article:
                record_add_field(rec, '024', ind1='7', subfields=[('a', related_article),
                                                                  ('2', 'DOI')])
        try:
            return record_xml_output(rec)
        except UnicodeDecodeError:
            message = "Found a bad char in the file for the article " + doi
            sys.stderr.write(message)
            return ""