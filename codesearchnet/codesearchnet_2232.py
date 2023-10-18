def process_docstring(app, what, name, obj, options, lines):
    """Enable markdown syntax in docstrings"""
    
    markdown = "\n".join(lines)

    # ast = cm_parser.parse(markdown)
    # html = cm_renderer.render(ast)
    rest = m2r(markdown)

    rest.replace("\r\n", "\n")
    del lines[:]
    lines.extend(rest.split("\n"))