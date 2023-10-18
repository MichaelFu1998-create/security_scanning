def _add_references(self, rec):
        """ Adds the reference to the record """
        for ref in self.document.getElementsByTagName('ref'):
            for ref_type, doi, authors, collaboration, journal, volume, page, year,\
                    label, arxiv, publisher, institution, unstructured_text,\
                    external_link, report_no, editors in self._get_reference(ref):
                subfields = []
                if doi:
                    subfields.append(('a', doi))
                for author in authors:
                    subfields.append(('h', author))
                for editor in editors:
                    subfields.append(('e', editor))
                if year:
                    subfields.append(('y', year))
                if unstructured_text:
                    if page:
                        subfields.append(('m', unstructured_text + ', ' + page))
                    else:
                        subfields.append(('m', unstructured_text))
                if collaboration:
                    subfields.append(('c', collaboration))
                if institution:
                    subfields.append(('m', institution))
                if publisher:
                    subfields.append(('p', publisher))
                if arxiv:
                    subfields.append(('r', arxiv))
                if report_no:
                    subfields.append(('r', report_no))
                if external_link:
                    subfields.append(('u', external_link))
                if label:
                    subfields.append(('o', label))
                if ref_type == 'book':
                    if journal:
                        subfields.append(('t', journal))
                    if volume:
                        subfields.append(('m', volume))
                    elif page and not unstructured_text:
                        subfields.append(('m', page))
                else:
                    if volume and page:
                        subfields.append(('s', journal + "," + volume + "," + page))
                    elif journal:
                        subfields.append(('t', journal))
                if ref_type:
                    subfields.append(('d', ref_type))
                if not subfields:
                    #misc-type references
                    try:
                        r = ref.getElementsByTagName('mixed-citation')[0]
                        text = xml_to_text(r)
                        label = text.split()[0]
                        text = " ".join(text.split()[1:])
                        subfields.append(('s', text))
                        record_add_field(rec, '999', ind1='C', ind2='5', subfields=subfields)
                    except IndexError:
                        #references without 'mixed-citation' tag
                        try:
                            r = ref.getElementsByTagName('note')[0]
                            subfields.append(('s', xml_to_text(r)))
                            record_add_field(rec, '999', ind1='C', ind2='5', subfields=subfields)
                        except IndexError:
                            #references without 'note' tag
                            subfields.append(('s', xml_to_text(ref)))
                            record_add_field(rec, '999', ind1='C', ind2='5', subfields=subfields)
                else:
                    record_add_field(rec, '999', ind1='C', ind2='5', subfields=subfields)