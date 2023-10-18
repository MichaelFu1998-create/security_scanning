def _get_reference(self, ref):
        """Retrieve the data for a reference."""
        label = get_value_in_tag(ref, 'label')
        label = re.sub('\D', '', label)
        for innerref in ref.getElementsByTagName('mixed-citation'):
            ref_type = innerref.getAttribute('publication-type')
            institution = get_value_in_tag(innerref, 'institution')
            report_no = ''
            for tag in innerref.getElementsByTagName('pub-id'):
                if tag.getAttribute('pub-id-type') == 'other':
                    if tag.hasChildNodes():
                        report_no = get_all_text(tag)
            doi = ''
            for tag in innerref.getElementsByTagName('pub-id'):
                if tag.getAttribute('pub-id-type') == 'doi':
                    doi = xml_to_text(tag)
            collaboration = get_value_in_tag(innerref, 'collab')
            authors = []
            person_groups = innerref.getElementsByTagName('person-group')
            for author_group in person_groups:
                if author_group.getAttribute('person-group-type') == 'author':
                    for author in author_group.getElementsByTagName('string-name'):
                        if author.hasChildNodes():
                            authors.append(get_all_text(author))
            editors = []
            for editor_group in person_groups:
                if editor_group.getAttribute('person-group-type') == 'editor':
                    for editor in editor_group.getElementsByTagName('string-name'):
                        if editor.hasChildNodes():
                            editors.append(get_all_text(editor))
            journal = get_value_in_tag(innerref, 'source')
            journal, volume = fix_journal_name(journal, self.journal_mappings)
            volume += get_value_in_tag(innerref, 'volume')
            if journal == 'J.High Energy Phys.' or journal == 'JHEP':
                issue = get_value_in_tag(innerref, 'issue')
                volume = volume[2:] + issue
                journal = 'JHEP'
            page = get_value_in_tag(innerref, 'page-range')
            year = get_value_in_tag(innerref, 'year')
            external_link = get_value_in_tag(innerref, 'ext-link')
            arxiv = ''
            for tag in innerref.getElementsByTagName('pub-id'):
                if tag.getAttribute('pub-id-type') == 'arxiv':
                    if tag.hasChildNodes():
                        arxiv = get_all_text(tag)
            arxiv = format_arxiv_id(arxiv)
            publisher = get_value_in_tag(innerref, 'publisher-name')
            publisher_location = get_value_in_tag(innerref, 'publisher-loc')
            if publisher_location:
                publisher = publisher_location + ': ' + publisher
            unstructured_text = []
            for child in innerref.childNodes:
                if child.nodeType == child.TEXT_NODE:
                    text = child.nodeValue.strip()
                    text = re.sub(r'[\[\]\(\.;\)]', '', text).strip()
                    if text.startswith(','):
                        text = text[1:].strip()
                    if text.endswith('Report No'):
                        text = institution + " " + text
                        institution = ''
                        text = text.strip()
                    elif text.endswith(' ed'):
                        text += '.'
                    elif text.endswith('PhD thesis,'):
                        if institution:
                            text += ' ' + institution
                            institution = ''
                        else:
                            text = text[:-1]
                    elif text.startswith('Seminar,'):
                        article_title = get_value_in_tag(innerref, 'article-title')
                        text = institution + " Seminar, \"" + article_title + "\""
                        institution = ''
                    elif text == u'\u201d':
                        text = ''
                    ignore_text = ['in', 'pp', 'edited by']
                    if text.startswith('Vol'):
                        temp = re.sub(r'\D', '', text)
                        if temp:
                            volume += temp
                    elif len(text) > 1 and text not in ignore_text\
                            and not (text.isdigit() or text[:-1].isdigit()):
                        unstructured_text.append(text)
            if unstructured_text:
                unstructured_text = " ".join(unstructured_text)
            if ref_type == 'book':
                if volume and not volume.lower().startswith('vol'):
                    volume = 'Vol ' + volume
                if volume and page:
                    volume = volume + ', pp ' + page
            yield ref_type, doi, authors, collaboration, journal, volume, page, year,\
                label, arxiv, publisher, institution, unstructured_text, external_link,\
                report_no, editors