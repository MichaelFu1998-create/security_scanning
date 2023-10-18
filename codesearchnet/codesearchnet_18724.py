def get_record(self, path=None, no_pdf=False,
                   test=False, refextract_callback=None):
        """Convert a record to MARCXML format.

        :param path: path to a record.
        :type path: string
        :param test: flag to determine if it is a test call.
        :type test: bool
        :param refextract_callback: callback to be used to extract
                                    unstructured references. It should
                                    return a marcxml formated string
                                    of the reference.
        :type refextract_callback: callable

        :returns: marcxml formated string.
        """
        xml_doc = self.get_article(path)
        rec = create_record()
        title = self.get_title(xml_doc)
        if title:
            record_add_field(rec, '245', subfields=[('a', title)])
        (journal, dummy, volume, issue, first_page, last_page, year,
         start_date, doi) = self.get_publication_information(xml_doc, path)
        if not journal:
            journal = self.get_article_journal(xml_doc)
        if start_date:
            record_add_field(rec, '260', subfields=[('c', start_date),
                                                    ('t', 'published')])
        else:
            record_add_field(
                rec, '260', subfields=[('c', time.strftime('%Y-%m-%d'))])
        if doi:
            record_add_field(rec, '024', ind1='7', subfields=[('a', doi),
                                                              ('2', 'DOI')])
        license, license_url = self.get_license(xml_doc)
        if license and license_url:
            record_add_field(rec, '540', subfields=[('a', license),
                                                    ('u', license_url)])
        elif license_url:
            record_add_field(rec, '540', subfields=[('u', license_url)])
        self.logger.info("Creating record: %s %s" % (path, doi))
        authors = self.get_authors(xml_doc)
        first_author = True
        for author in authors:
            author_name = (author['surname'], author.get(
                'given_name') or author.get('initials'))
            subfields = [('a', '%s, %s' % author_name)]
            if 'orcid' in author:
                subfields.append(('j', author['orcid']))
            if 'affiliation' in author:
                for aff in author["affiliation"]:
                    subfields.append(('v', aff))

                if self.extract_nations:
                    add_nations_field(subfields)

            if author.get('email'):
                subfields.append(('m', author['email']))
            if first_author:
                record_add_field(rec, '100', subfields=subfields)
                first_author = False
            else:
                record_add_field(rec, '700', subfields=subfields)

        abstract = self.get_abstract(xml_doc)
        if abstract:
            record_add_field(rec, '520', subfields=[('a', abstract),
                                                    ('9', 'Elsevier')])
        record_copyright = self.get_copyright(xml_doc)
        if record_copyright:
            record_add_field(rec, '542', subfields=[('f', record_copyright)])
        keywords = self.get_keywords(xml_doc)
        if self.CONSYN:
            for tag in xml_doc.getElementsByTagName('ce:collaboration'):
                collaboration = get_value_in_tag(tag, 'ce:text')
                if collaboration:
                    record_add_field(rec, '710',
                                     subfields=[('g', collaboration)])

            # We add subjects also as author keywords
            subjects = xml_doc.getElementsByTagName('dct:subject')
            for subject in subjects:
                for listitem in subject.getElementsByTagName('rdf:li'):
                    keyword = xml_to_text(listitem)
                    if keyword not in keywords:
                        keywords.append(keyword)
            for keyword in keywords:
                record_add_field(rec, '653', ind1='1',
                                 subfields=[('a', keyword),
                                            ('9', 'author')])
            journal, dummy = fix_journal_name(journal.strip(),
                                              self.journal_mappings)
            subfields = []
            doctype = self.get_doctype(xml_doc)
            try:
                page_count = int(last_page) - int(first_page) + 1
                record_add_field(rec, '300',
                                 subfields=[('a', str(page_count))])
            except ValueError:  # do nothing
                pass
            if doctype == 'err':
                subfields.append(('m', 'Erratum'))
            elif doctype == 'add':
                subfields.append(('m', 'Addendum'))
            elif doctype == 'pub':
                subfields.append(('m', 'Publisher Note'))
            elif doctype == 'rev':
                record_add_field(rec, '980', subfields=[('a', 'Review')])
            if journal:
                subfields.append(('p', journal))
            if first_page and last_page:
                subfields.append(('c', '%s-%s' %
                                       (first_page, last_page)))
            elif first_page:
                subfields.append(('c', first_page))
            if volume:
                subfields.append(('v', volume))
            if year:
                subfields.append(('y', year))
            record_add_field(rec, '773', subfields=subfields)
            if not test:
                if license:
                    url = 'http://www.sciencedirect.com/science/article/pii/'\
                          + path.split('/')[-1][:-4]
                    record_add_field(rec, '856', ind1='4',
                                     subfields=[('u', url),
                                                ('y', 'Elsevier server')])
                    record_add_field(rec, 'FFT', subfields=[('a', path),
                                                            ('t', 'INSPIRE-PUBLIC'),
                                                            ('d', 'Fulltext')])
                else:
                    record_add_field(rec, 'FFT', subfields=[('a', path),
                                                            ('t', 'Elsevier'),
                                                            ('o', 'HIDDEN')])
            record_add_field(rec, '980', subfields=[('a', 'HEP')])
            record_add_field(rec, '980', subfields=[('a', 'Citeable')])
            record_add_field(rec, '980', subfields=[('a', 'Published')])
            self._add_references(xml_doc, rec, refextract_callback)
        else:
            licence = 'http://creativecommons.org/licenses/by/3.0/'
            record_add_field(rec,
                             '540',
                             subfields=[('a', 'CC-BY-3.0'), ('u', licence)])
            if keywords:
                for keyword in keywords:
                    record_add_field(
                        rec, '653', ind1='1', subfields=[('a', keyword),
                                    ('9', 'author')])

            pages = ''
            if first_page and last_page:
                pages = '{0}-{1}'.format(first_page, last_page)
            elif first_page:
                pages = first_page

            subfields = filter(lambda x: x[1] and x[1] != '-', [('p', journal),
                                                                ('v', volume),
                                                                ('n', issue),
                                                                ('c', pages),
                                                                ('y', year)])

            record_add_field(rec, '773', subfields=subfields)
            if not no_pdf:
                from invenio.search_engine import perform_request_search
                query = '0247_a:"%s" AND NOT 980:DELETED"' % (doi,)
                prev_version = perform_request_search(p=query)

                old_pdf = False

                if prev_version:
                    from invenio.bibdocfile import BibRecDocs
                    prev_rec = BibRecDocs(prev_version[0])
                    try:
                        pdf_path = prev_rec.get_bibdoc('main')
                        pdf_path = pdf_path.get_file(
                            ".pdf;pdfa", exact_docformat=True)
                        pdf_path = pdf_path.fullpath
                        old_pdf = True
                        record_add_field(rec, 'FFT',
                                         subfields=[('a', pdf_path),
                                                    ('n', 'main'),
                                                    ('f', '.pdf;pdfa')])
                        message = ('Leaving previously delivered PDF/A for: '
                                   + doi)
                        self.logger.info(message)
                    except:
                        pass
                try:
                    if exists(join(path, 'main_a-2b.pdf')):
                        pdf_path = join(path, 'main_a-2b.pdf')
                        record_add_field(rec, 'FFT',
                                         subfields=[('a', pdf_path),
                                                    ('n', 'main'),
                                                    ('f', '.pdf;pdfa')])
                        self.logger.debug('Adding PDF/A to record: %s'
                                          % (doi,))
                    elif exists(join(path, 'main.pdf')):
                        pdf_path = join(path, 'main.pdf')
                        record_add_field(rec, 'FFT', subfields=[('a', pdf_path)])
                    else:
                        if not old_pdf:
                            message = "Record " + doi
                            message += " doesn't contain PDF file."
                            self.logger.warning(message)
                            raise MissingFFTError(message)
                except MissingFFTError:
                    message = "Elsevier paper: %s is missing PDF." % (doi,)
                    register_exception(alert_admin=True, prefix=message)
                version = self.get_elsevier_version(find_package_name(path))
                record_add_field(rec, '583', subfields=[('l', version)])
                xml_path = join(path, 'main.xml')
                record_add_field(rec, 'FFT', subfields=[('a', xml_path)])
                record_add_field(rec, '980', subfields=[('a', 'SCOAP3'),
                                                        ('b', 'Elsevier')])
        try:
            return record_xml_output(rec)
        except UnicodeDecodeError:
            message = "Found a bad char in the file for the article " + doi
            sys.stderr.write(message)
            return ""