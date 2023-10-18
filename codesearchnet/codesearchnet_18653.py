def fix_name_capitalization(lastname, givennames):
    """ Converts capital letters to lower keeps first letter capital. """
    lastnames = lastname.split()
    if len(lastnames) == 1:
        if '-' in lastname:
            names = lastname.split('-')
            names = map(lambda a: a[0] + a[1:].lower(), names)
            lastname = '-'.join(names)
        else:
            lastname = lastname[0] + lastname[1:].lower()
    else:
        names = []
        for name in lastnames:
            if re.search(r'[A-Z]\.', name):
                names.append(name)
            else:
                names.append(name[0] + name[1:].lower())
        lastname = ' '.join(names)
        lastname = collapse_initials(lastname)
    names = []
    for name in givennames:
        if re.search(r'[A-Z]\.', name):
            names.append(name)
        else:
            names.append(name[0] + name[1:].lower())
    givennames = ' '.join(names)
    return lastname, givennames