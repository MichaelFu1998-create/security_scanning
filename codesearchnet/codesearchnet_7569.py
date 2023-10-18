def codestr2rst(codestr, lang='python'):
    """Return reStructuredText code block from code string"""
    code_directive = "\n.. code-block:: {0}\n\n".format(lang)
    indented_block = indent(codestr, ' ' * 4)
    return code_directive + indented_block