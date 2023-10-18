def prompt(question, choices=None):
    """echo a prompt to the user and wait for an answer

    question -- string -- the prompt for the user
    choices -- list -- if given, only exit when prompt matches one of the choices
    return -- string -- the answer that was given by the user
    """

    if not re.match("\s$", question):
        question = "{}: ".format(question)

    while True:
        if sys.version_info[0] > 2:
            answer = input(question)

        else:
            answer = raw_input(question)

        if not choices or answer in choices:
            break

    return answer