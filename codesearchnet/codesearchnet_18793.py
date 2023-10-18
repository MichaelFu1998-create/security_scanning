def record_xml_output(rec, tags=None, order_fn=None):
    """Generate the XML for record 'rec'.

    :param rec: record
    :param tags: list of tags to be printed
    :return: string
    """
    if tags is None:
        tags = []
    if isinstance(tags, str):
        tags = [tags]
    if tags and '001' not in tags:
        # Add the missing controlfield.
        tags.append('001')

    marcxml = ['<record>']

    # Add the tag 'tag' to each field in rec[tag]
    fields = []
    if rec is not None:
        for tag in rec:
            if not tags or tag in tags:
                for field in rec[tag]:
                    fields.append((tag, field))
        if order_fn is None:
            record_order_fields(fields)
        else:
            record_order_fields(fields, order_fn)
        for field in fields:
            marcxml.append(field_xml_output(field[1], field[0]))
    marcxml.append('</record>')
    return '\n'.join(marcxml)