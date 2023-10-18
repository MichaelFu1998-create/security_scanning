def pruneUI(dupeList, mainPos=1, mainLen=1):
    """Display a list of files and prompt for ones to be kept.

    The user may enter ``all`` or one or more numbers separated by spaces
    and/or commas.

    .. note:: It is impossible to accidentally choose to keep none of the
        displayed files.

    :param dupeList: A list duplicate file paths
    :param mainPos: Used to display "set X of Y"
    :param mainLen: Used to display "set X of Y"
    :type dupeList: :class:`~__builtins__.list`
    :type mainPos: :class:`~__builtins__.int`
    :type mainLen: :class:`~__builtins__.int`

    :returns: A list of files to be deleted.
    :rtype: :class:`~__builtins__.int`
    """
    dupeList = sorted(dupeList)
    print
    for pos, val in enumerate(dupeList):
        print "%d) %s" % (pos + 1, val)
    while True:
        choice = raw_input("[%s/%s] Keepers: " % (mainPos, mainLen)).strip()
        if not choice:
            print ("Please enter a space/comma-separated list of numbers or "
                   "'all'.")
            continue
        elif choice.lower() == 'all':
            return []
        try:
            out = [int(x) - 1 for x in choice.replace(',', ' ').split()]
            return [val for pos, val in enumerate(dupeList) if pos not in out]
        except ValueError:
            print("Invalid choice. Please enter a space/comma-separated list"
                  "of numbers or 'all'.")