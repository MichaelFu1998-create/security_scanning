def find_item_by_name(list_, namegetter, name):
    """
    Find a item a given list by a matching name.

    The search for the name is done in this relaxing way:

    - exact name match
    - case-insentive name match
    - attribute starts with the name
    - attribute starts with the name (case insensitive)
    - name appears in the attribute
    - name appears in the attribute (case insensitive)

    :param    list_: A list of elements
    :type     list_: ``list``

    :param    namegetter: Function that returns the name for a given
                          element in the list
    :type     namegetter: ``function``

    :param    name: Name to search for
    :type     name: ``str``

    """
    matching_items = [i for i in list_ if namegetter(i) == name]
    if not matching_items:
        prog = re.compile(re.escape(name) + '$', re.IGNORECASE)
        matching_items = [i for i in list_ if prog.match(namegetter(i))]
    if not matching_items:
        prog = re.compile(re.escape(name))
        matching_items = [i for i in list_ if prog.match(namegetter(i))]
    if not matching_items:
        prog = re.compile(re.escape(name), re.IGNORECASE)
        matching_items = [i for i in list_ if prog.match(namegetter(i))]
    if not matching_items:
        prog = re.compile(re.escape(name))
        matching_items = [i for i in list_ if prog.search(namegetter(i))]
    if not matching_items:
        prog = re.compile(re.escape(name), re.IGNORECASE)
        matching_items = [i for i in list_ if prog.search(namegetter(i))]
    return matching_items