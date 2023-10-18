def _colorize(output):
    """
    Return `output` colorized with Pygments, if available.

    """
    if not pygments:
        return output
    # Available styles
    # ['monokai', 'manni', 'rrt', 'perldoc', 'borland', 'colorful', 'default',
    # 'murphy', 'vs', 'trac', 'tango', 'fruity', 'autumn', 'bw', 'emacs',
    # 'vim', 'pastie', 'friendly', 'native']
    return pygments.highlight(output,
            pygments.lexers.PythonLexer(),
            pygments.formatters.Terminal256Formatter(style='monokai'))