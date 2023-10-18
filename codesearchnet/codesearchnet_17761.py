def input_with_prefill(prompt, text):
    '''
    https://stackoverflow.com/questions/8505163/is-it-possible-to-prefill-a-input-in-python-3s-command-line-interface
    '''
    def hook():
        readline.insert_text(text)
        readline.redisplay()
    try:
        readline.set_pre_input_hook(hook)
    except Exception:
        pass
    result = input(prompt)
    try:
        readline.set_pre_input_hook()
    except Exception:
        pass
    return result