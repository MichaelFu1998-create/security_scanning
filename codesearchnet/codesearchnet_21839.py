def launch(prompt_prefix=None):
    '''Launch a subshell'''

    if prompt_prefix:
        os.environ['PROMPT'] = prompt(prompt_prefix)

    subprocess.call(cmd(), env=os.environ.data)