def remove_function_signature_type_comment(body):
    """Removes the legacy signature type comment, leaving other comments if any."""
    for node in body.children:
        if node.type == token.INDENT:
            prefix = node.prefix.lstrip()
            if prefix.startswith('# type: '):
                node.prefix = '\n'.join(prefix.split('\n')[1:])
            break