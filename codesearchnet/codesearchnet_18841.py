def get_record(self, xml_file):
        """ Reads a xml file in JATS format and returns
            a xml string in marc format """
        self.document = parse(xml_file)

        if get_value_in_tag(self.document, "meta"):
            raise ApsPackageXMLError("The XML format of %s is not correct"
                                     % (xml_file,))
        page_count = self._get_page_count()
        rec = create_record()
        if page_count:
            record_add_field(rec, '300', subfields=[('a', page_count)])
        pacscodes = self._get_pacscodes()
        for pacscode in pacscodes:
            record_add_field(rec, '084', subfields=[('2', 'PACS'),
                                                    ('a', pacscode)])
        subject = self._get_subject()
        if subject:
            record_add_field(rec, '650', ind1='1', ind2='7', subfields=[('2', 'APS'),
                                                                        ('a', subject)])
        keywords = self._get_keywords()
        if keywords:
            record_add_field(rec, '653', ind1='1', subfields=[('a', ', '.join(keywords)),
                                                              ('9', 'author')])
        title, subtitle, _ = self._get_title()
        subfields = []
        if subtitle:
            subfields.append(('b', subtitle))
        if title:
            subfields.append(('a', title))
            record_add_field(rec, '245', subfields=subfields)
        journal, volume, issue, year, start_date, doi,\
            article_id, _, _ = self._get_publication_information()
        if start_date:
            record_add_field(rec, '260', subfields=[('c', start_date),
                                                    ('t', 'published')])
        if doi:
            record_add_field(rec, '024', ind1='7', subfields=[('a', doi),
                                                              ('2', 'DOI')])
        abstract = self._get_abstract()
        if abstract:
            record_add_field(rec, '520', subfields=[('a', abstract),
                                                    ('9', 'APS')])
        license, license_type, license_url = self._get_license()
        subfields = []
        if license:
            subfields.append(('a', license))
        if license_url:
            subfields.append(('u', license_url))
        if subfields:
            record_add_field(rec, '540', subfields=subfields)
        c_holder, c_year, c_statement = self._get_copyright()
        c_holder, c_year, c_statement = self._get_copyright()
        if c_holder and c_year:
            record_add_field(rec, '542', subfields=[('d', c_holder),
                                                    ('g', c_year),
                                                    ('e', 'Article')])
        elif c_statement:
            record_add_field(rec, '542', subfields=[('f', c_statement),
                                                    ('e', 'Article')])
        record_add_field(rec, '773', subfields=[('p', journal),
                                                ('v', volume),
                                                ('n', issue),
                                                ('y', year),
                                                ('c', article_id)])
        record_add_field(rec, '980', subfields=[('a', 'HEP')])
        record_add_field(rec, '980', subfields=[('a', 'Citeable')])
        record_add_field(rec, '980', subfields=[('a', 'Published')])
        self._add_authors(rec)
        self._add_references(rec)
        try:
            return record_xml_output(rec)
        except UnicodeDecodeError:
            sys.stderr.write("""Found a bad char in the file
                                for the article """ + doi)
            return ""