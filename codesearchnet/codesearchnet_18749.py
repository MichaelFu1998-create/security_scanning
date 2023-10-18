def get_record_rich(self, filename, ref_extract_callback=None):
        """
        Gets the Marc xml of the files in xaml_rich directory

        :param fileName: the name of the file to parse.
        :type fileName: string

        :returns: a string with the marc xml version of the file.
        """
        self.document = parse(filename)
        rec = create_record()
        articles = self.document.getElementsByTagName('ArticleID')
        for article in articles:
            article_type = article.getAttribute('Type')
            if not article_type == 'Article':
                return ''
            doi = get_value_in_tag(self.document, 'DOI')
            date = ''
            for tag in self.document.getElementsByTagName('Accepted'):
                year = get_value_in_tag(tag, 'Year')
                month = get_value_in_tag(tag, 'Month').zfill(2)
                day = get_value_in_tag(tag, 'Day').zfill(2)
                date = "%s-%s-%s" % (year, month, day)
            if not date:
                for tag in self.document.getElementsByTagName('OnlineDate'):
                    year = get_value_in_tag(tag, 'Year')
                    month = get_value_in_tag(tag, 'Month').zfill(2)
                    day = get_value_in_tag(tag, 'Day').zfill(2)
                    date = "%s-%s-%s" % (year, month, day)
            first_page = get_value_in_tag(article, 'FirstPage')
            last_page = get_value_in_tag(article, 'LastPage')
            subjects = article.getElementsByTagName('Keyword')
            subjects = map(xml_to_text, subjects)
            subject = ', '.join(subjects)
            copyright_statement = get_value_in_tag(article, 'Copyright')
        journal = get_value_in_tag(self.document, 'JournalTitle')
        journal, volume = fix_journal_name(journal, self.journal_mappings)
        issues = self.document.getElementsByTagName('IssueID')
        for issue in issues:
            volume += get_value_in_tag(issue, 'Volume')
            year = get_value_in_tag(issue, 'Year')
        title = get_value_in_tag(self.document, 'Title')
        authors = self.document.getElementsByTagName('Author')
        affiliations = self.document.getElementsByTagName('Affiliation')

        def affiliation_pair(a):
            return a.getAttribute('ID'), get_value_in_tag(
                a, 'UnstructuredAffiliation'
            )

        affiliations = map(affiliation_pair, affiliations)
        affiliations = dict(affiliations)

        def author_pair(a):
            surname = get_value_in_tag(a, 'LastName')
            first_name = get_value_in_tag(a, 'FirstName')
            middle_name = get_value_in_tag(a, 'MiddleName')
            if middle_name:
                name = '%s, %s %s' % (surname, first_name, middle_name)
            else:
                name = '%s, %s' % (surname, first_name)
            try:
                affid = a.getElementsByTagName(
                    'AffiliationID'
                )[0].getAttribute('Label')
                affiliation = affiliations[affid]
            except IndexError:
                affiliation = ''
            except KeyError:
                affiliation = ''
            return name, affiliation

        authors = map(author_pair, authors)
        abstract = get_value_in_tag(self.document, 'Abstract')
        references = self.document.getElementsByTagName('Bibliomixed')

        for reference in references:
            subfields = []
            label = reference.getAttribute('N')
            if label:
                subfields.append(('o', label))
            bibliosets = reference.getElementsByTagName('Biblioset')
            for tag in bibliosets:
                ref_year = get_value_in_tag(tag, 'Date')
                ref_journal = get_value_in_tag(tag, 'JournalShortTitle')
                ref_journal, ref_volume = fix_journal_name(
                    ref_journal, self.journal_mappings
                )
                ref_volume += get_value_in_tag(tag, 'Volume')
                ref_page = get_value_in_tag(tag, 'ArtPageNums')
                if ref_year:
                    subfields.append(('y', ref_year))
                if ref_journal and ref_volume and ref_page:
                    subfields.append(('s', '%s,%s,%s' % (ref_journal,
                                                         ref_volume,
                                                         ref_page)))
                reference.removeChild(tag)
            text_ref = xml_to_text(reference)
            if ref_extract_callback:
                ref_xml = ref_extract_callback(text_ref)
                dom = parseString(ref_xml)
                fields = dom.getElementsByTagName("datafield")[0]
                fields = fields.getElementsByTagName("subfield")
                if fields:
                    subfields.append(('9', 'refextract'))
                for field in fields:
                    data = field.firstChild.data
                    code = field.getAttribute("code")
                    if code == 'm' and bibliosets:
                        continue
                    else:
                        subfields.append((code, data))
            else:
                subfields.append(('m', text_ref))
            if subfields:
                record_add_field(rec, '999', ind1='C', ind2='5',
                                 subfields=subfields)

        if title:
            record_add_field(rec, '245', subfields=[('a', title)])
        if date:
            record_add_field(rec, '260', subfields=[('c', date),
                                                    ('t', 'published')])
        if doi:
            record_add_field(rec, '024', ind1='7', subfields=[('a', doi),
                                                              ('2', 'DOI')])
        if abstract:
            record_add_field(rec, '520', subfields=[('a', abstract),
                                                    ('9', 'EDPSciences')])
        first_author = True
        for author in authors:
            if first_author:
                subfields = [('a', author[0])]
                if author[1]:
                    subfields.append(('v', author[1]))
                record_add_field(rec, '100', subfields=subfields)
                first_author = False
            else:
                subfields = [('a', author[0])]
                if author[1]:
                    subfields.append(('v', author[1]))
                record_add_field(rec, '700', subfields=subfields)
        subfields = []
        if journal and volume and first_page:
            subfields.append(('s', "%s,%s,%s" % (journal,
                                                 volume,
                                                 first_page)))
        if first_page and last_page:
            try:
                nuber_of_pages = int(last_page) - int(first_page)
                record_add_field(rec, '300',
                                 subfields=[('a', str(nuber_of_pages))])
            except ValueError:
                pass
            subfields.append(('c', '%s-%s' % (first_page,
                                              last_page)))
        if year:
            subfields.append(('y', year))
        record_add_field(rec, '773', subfields=subfields)
        record_add_field(rec, '980', subfields=[('a', 'HEP')])
        if copyright_statement:
            record_add_field(rec, '542',
                             subfields=[('f', copyright_statement)])
        if subject:
            record_add_field(rec, '650', ind1='1', ind2='7',
                             subfields=[('2', 'EDPSciences'),
                                        ('a', subject)])
        try:
            return record_xml_output(rec)
        except UnicodeDecodeError:
            message = "Found a bad char in the file for the article " + doi
            sys.stderr.write(message)
            return ""