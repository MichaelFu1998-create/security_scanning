def record_add_field(rec, tag, ind1='', ind2='', subfields=[],
                     controlfield_value=''):
    """Add a MARCXML datafield as a new child to a XML document."""
    if controlfield_value:
        doc = etree.Element("controlfield",
                            attrib={
                                "tag": tag,
                            })
        doc.text = unicode(controlfield_value)
    else:
        doc = etree.Element("datafield",
                            attrib={
                                "tag": tag,
                                "ind1": ind1,
                                "ind2": ind2,
                            })
        for code, value in subfields:
            field = etree.SubElement(doc, "subfield", attrib={"code": code})
            field.text = value
    rec.append(doc)
    return rec