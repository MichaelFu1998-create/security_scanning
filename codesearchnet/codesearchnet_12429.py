def raw(prompt, *args, **kwargs):
    """Calls input to allow user to input an arbitrary string. User can go
    back by entering the `go_back` string. Works in both Python 2 and 3.
    """
    go_back = kwargs.get('go_back', '<')
    type_ = kwargs.get('type', str)
    default = kwargs.get('default', '')
    with stdout_redirected(sys.stderr):
        while True:
            try:
                if kwargs.get('secret', False):
                    answer = getpass.getpass(prompt)
                elif sys.version_info < (3, 0):
                    answer = raw_input(prompt)
                else:
                    answer = input(prompt)

                if not answer:
                    answer = default

                if answer == go_back:
                    raise QuestionnaireGoBack
                return type_(answer)
            except ValueError:
                eprint('\n`{}` is not a valid `{}`\n'.format(answer, type_))