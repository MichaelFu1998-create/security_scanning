def element_tree_collection_to_records(tree):
    """Take an ElementTree and converts the nodes into BibRecord records.

    This function is for a tree root of collection as such:
    <collection>
        <record>
            <!-- MARCXML -->
        </record>
        <record> ... </record>
    </collection>
    """
    from .bibrecord import create_record

    records = []
    collection = tree.getroot()
    for record_element in collection.getchildren():
        marcxml = ET.tostring(record_element, encoding="utf-8")
        record, status, errors = create_record(marcxml)
        if errors:
            print(str(status))
        records.append(record)
    return records