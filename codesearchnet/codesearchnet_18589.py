def element_tree_oai_records(tree, header_subs=None):
    """Take an ElementTree and converts the nodes into BibRecord records.

    This expects a clean OAI response with the tree root as ListRecords
    or GetRecord and record as the subtag like so:
    <ListRecords|GetRecord>
        <record>
            <header>
                <!-- Record Information -->
            </header>
            <metadata>
                <record>
                    <!-- MARCXML -->
                </record>
            </metadata>
        </record>
        <record> ... </record>
    </ListRecords|GetRecord>

    :param tree: ElementTree object corresponding to GetRecord node from
                 OAI request
    :param header_subs: OAI header subfields, if any

    :yield: (record, is_deleted) A tuple, with first a BibRecord found and
             second a boolean value saying if this is a deleted record or not.
    """
    from .bibrecord import record_add_field, create_record

    if not header_subs:
        header_subs = []
    # Make it a tuple, this information should not be changed
    header_subs = tuple(header_subs)

    oai_records = tree.getroot()
    for record_element in oai_records.getchildren():
        header = record_element.find('header')

        # Add to OAI subfield
        datestamp = header.find('datestamp')
        identifier = header.find('identifier')
        identifier = identifier.text

        # The record's subfield is based on header information
        subs = list(header_subs)
        subs.append(("a", identifier))
        subs.append(("d", datestamp.text))

        if "status" in header.attrib and header.attrib["status"] == "deleted":
            # Record was deleted - create delete record
            deleted_record = {}
            record_add_field(deleted_record, "037", subfields=subs)
            yield deleted_record, True
        else:
            marc_root = record_element.find('metadata').find('record')
            marcxml = ET.tostring(marc_root, encoding="utf-8")
            record, status, errors = create_record(marcxml)
            if status == 1:
                # Add OAI request information
                record_add_field(record, "035", subfields=subs)
                yield record, False