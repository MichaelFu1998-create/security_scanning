def _find_sections(md_ast, sections, last, last_class, total_lines=None):
    """
    Walks through a CommonMark AST to find section headers that delineate
    content that should be updated by this script

    :param md_ast:
        The AST of the markdown document

    :param sections:
        A dict to store the start and end lines of a section. The key will be
        a two-element tuple of the section type ("class", "function",
        "method" or "attribute") and identifier. The values are a two-element
        tuple of the start and end line number in the markdown document of the
        section.

    :param last:
        A dict containing information about the last section header seen.
        Includes the keys "type_name", "identifier", "start_line".

    :param last_class:
        A unicode string of the name of the last class found - used when
        processing methods and attributes.

    :param total_lines:
        An integer of the total number of lines in the markdown document -
        used to work around a bug in the API of the Python port of CommonMark
    """

    def child_walker(node):
        for child, entering in node.walker():
            if child == node:
                continue
            yield child, entering

    for child, entering in child_walker(md_ast):
        if child.t == 'heading':
            start_line = child.sourcepos[0][0]

            if child.level == 2:
                if last:
                    sections[(last['type_name'], last['identifier'])] = (last['start_line'], start_line - 1)
                    last.clear()

            if child.level in set([3, 5]):
                heading_elements = []
                for heading_child, _ in child_walker(child):
                    heading_elements.append(heading_child)
                if len(heading_elements) != 2:
                    continue
                first = heading_elements[0]
                second = heading_elements[1]
                if first.t != 'code':
                    continue
                if second.t != 'text':
                    continue

                type_name = second.literal.strip()
                identifier = first.literal.strip().replace('()', '').lstrip('.')

                if last:
                    sections[(last['type_name'], last['identifier'])] = (last['start_line'], start_line - 1)
                    last.clear()

                if type_name == 'function':
                    if child.level != 3:
                        continue

                if type_name == 'class':
                    if child.level != 3:
                        continue
                    last_class.append(identifier)

                if type_name in set(['method', 'attribute']):
                    if child.level != 5:
                        continue
                    identifier = last_class[-1] + '.' + identifier

                last.update({
                    'type_name': type_name,
                    'identifier': identifier,
                    'start_line': start_line,
                })

        elif child.t == 'block_quote':
            find_sections(child, sections, last, last_class)

    if last:
        sections[(last['type_name'], last['identifier'])] = (last['start_line'], total_lines)