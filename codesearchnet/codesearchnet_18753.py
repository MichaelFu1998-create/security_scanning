def add_cms_link(self):
        """Special handling if record is a CMS NOTE."""
        intnote = record_get_field_values(self.record, '690',
                                          filter_subfield_code="a",
                                          filter_subfield_value='INTNOTE')
        if intnote:
            val_088 = record_get_field_values(self.record,
                                              tag='088',
                                              filter_subfield_code="a")
            for val in val_088:
                if 'CMS' in val:
                    url = ('http://weblib.cern.ch/abstract?CERN-CMS' +
                           val.split('CMS', 1)[-1])
                    record_add_field(self.record,
                                     tag='856',
                                     ind1='4',
                                     subfields=[('u', url)])