def field_xml_output(field, tag):
    """Generate the XML for field 'field' and returns it as a string."""
    marcxml = []
    if field[3]:
        marcxml.append('  <controlfield tag="%s">%s</controlfield>' %
                       (tag, MathMLParser.html_to_text(field[3])))
    else:
        marcxml.append('  <datafield tag="%s" ind1="%s" ind2="%s">' %
                       (tag, field[1], field[2]))
        marcxml += [_subfield_xml_output(subfield) for subfield in field[0]]
        marcxml.append('  </datafield>')
    return '\n'.join(marcxml)