def is_valid_identifier(name):
    """Pedantic yet imperfect. Test to see if "name" is a valid python identifier
    """
    if not isinstance(name, str):
        return False
    if '\n' in name:
        return False
    if name.strip() != name:
        return False
    try:
        code = compile('\n{0}=None'.format(name), filename='<string>', mode='single')
        exec(code)
        return True
    except SyntaxError:
        return False