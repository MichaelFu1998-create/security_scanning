def record_xml_output(rec, pretty=True):
    """Given a document, return XML prettified."""
    from .html_utils import MathMLParser
    ret = etree.tostring(rec, xml_declaration=False)

    # Special MathML handling
    ret = re.sub("(&lt;)(([\/]?{0}))".format("|[\/]?".join(MathMLParser.mathml_elements)), '<\g<2>', ret)
    ret = re.sub("&gt;", '>', ret)
    if pretty:
        # We are doing our own prettyfication as etree pretty_print is too insane.
        ret = ret.replace('</datafield>', '  </datafield>\n')
        ret = re.sub(r'<datafield(.*?)>', r'  <datafield\1>\n', ret)
        ret = ret.replace('</subfield>', '</subfield>\n')
        ret = ret.replace('<subfield', '    <subfield')
        ret = ret.replace('record>', 'record>\n')
    return ret