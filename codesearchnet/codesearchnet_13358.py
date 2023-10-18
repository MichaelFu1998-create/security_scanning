def xml_elements_equal(element1, element2, ignore_level1_cdata = False):
    """Check if two XML elements are equal.

    :Parameters:
        - `element1`: the first element to compare
        - `element2`: the other element to compare
        - `ignore_level1_cdata`: if direct text children of the elements
          should be ignored for the comparision
    :Types:
        - `element1`: :etree:`ElementTree.Element`
        - `element2`: :etree:`ElementTree.Element`
        - `ignore_level1_cdata`: `bool`

    :Returntype: `bool`
    """
    # pylint: disable-msg=R0911
    if None in (element1, element2) or element1.tag != element2.tag:
        return False
    attrs1 = element1.items()
    attrs1.sort()
    attrs2 = element2.items()
    attrs2.sort()

    if not ignore_level1_cdata:
        if element1.text != element2.text:
            return False

    if attrs1 != attrs2:
        return False

    if len(element1) != len(element2):
        return False
    for child1, child2 in zip(element1, element2):
        if child1.tag != child2.tag:
            return False
        if not ignore_level1_cdata:
            if element1.text != element2.text:
                return False
        if not xml_elements_equal(child1, child2):
            return False
    return True