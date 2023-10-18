def build(surname, name, birthday, sex, municipality):
    """``build(surname, name, birthday, sex, municipality) -> string``

    Computes the fiscal code for the given person data.

    eg: build('Rocca', 'Emanuele', datetime.datetime(1983, 11, 18), 'M', 'D969') 
        -> RCCMNL83S18D969H
    """

    # RCCMNL
    output = __surname_triplet(surname) + __name_triplet(name)

    # RCCMNL83
    output += str(birthday.year)[2:]

    # RCCMNL83S
    output += MONTHSCODE[birthday.month - 1]

    # RCCMNL83S18
    output += "%02d" % (sex.upper() == 'M' and birthday.day or 40 + birthday.day)

    # RCCMNL83S18D969 
    output += municipality

    # RCCMNL83S18D969H
    output += control_code(output)

    assert isvalid(output)

    return output