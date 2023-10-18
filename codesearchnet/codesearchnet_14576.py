def ask(question, options, default):
    """
    Ask the user a question with a list of allowed answers (like yes or no).

    The user is presented with a question and asked to select an answer from
    the given options list. The default will be returned if the user enters
    nothing. The user is asked to repeat his answer if his answer does not
    match any of the allowed anwsers.

    :param    question: Question to present to the user (without question mark)
    :type     question: ``str``

    :param    options: List of allowed anwsers
    :type     options: ``list``

    :param    default: Default answer (if the user enters no text)
    :type     default: ``str``

    """
    assert default in options

    question += " ({})? ".format("/".join(o.upper() if o == default else o for o in options))
    selected = None
    while selected not in options:
        selected = input(question).strip().lower()
        if selected == "":
            selected = default
        else:
            if selected not in options:
                question = "Please type '{}'{comma} or '{}': ".format(
                    "', '".join(options[:-1]), options[-1],
                    comma=',' if len(options) > 2 else '',
                )
    return selected