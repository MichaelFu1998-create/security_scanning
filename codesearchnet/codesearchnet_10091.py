def run():
    """
    Looks through the docs/ dir and parses each markdown document, looking for
    sections to update from Python docstrings. Looks for section headers in
    the format:

     - ### `ClassName()` class
     - ##### `.method_name()` method
     - ##### `.attribute_name` attribute
     - ### `function_name()` function

    The markdown content following these section headers up until the next
    section header will be replaced by new markdown generated from the Python
    docstrings of the associated source files.

    By default maps docs/{name}.md to {modulename}/{name}.py. Allows for
    custom mapping via the md_source_map variable.
    """

    print('Updating API docs...')

    md_files = []
    for root, _, filenames in os.walk(os.path.join(package_root, 'docs')):
        for filename in filenames:
            if not filename.endswith('.md'):
                continue
            md_files.append(os.path.join(root, filename))

    parser = CommonMark.Parser()

    for md_file in md_files:
        md_file_relative = md_file[len(package_root) + 1:]
        if md_file_relative in md_source_map:
            py_files = md_source_map[md_file_relative]
            py_paths = [os.path.join(package_root, py_file) for py_file in py_files]
        else:
            py_files = [os.path.basename(md_file).replace('.md', '.py')]
            py_paths = [os.path.join(package_root, package_name, py_files[0])]

            if not os.path.exists(py_paths[0]):
                continue

        with open(md_file, 'rb') as f:
            markdown = f.read().decode('utf-8')

        original_markdown = markdown
        md_lines = list(markdown.splitlines())
        md_ast = parser.parse(markdown)

        last_class = []
        last = {}
        sections = OrderedDict()
        find_sections(md_ast, sections, last, last_class, markdown.count("\n") + 1)

        md_chunks = {}

        for index, py_file in enumerate(py_files):
            py_path = py_paths[index]

            with open(os.path.join(py_path), 'rb') as f:
                code = f.read().decode('utf-8')
                module_ast = ast.parse(code, filename=py_file)
                code_lines = list(code.splitlines())

            for node in ast.iter_child_nodes(module_ast):
                walk_ast(node, code_lines, sections, md_chunks)

        added_lines = 0

        def _replace_md(key, sections, md_chunk, md_lines, added_lines):
            start, end = sections[key]
            start -= 1
            start += added_lines
            end += added_lines
            new_lines = md_chunk.split('\n')
            added_lines += len(new_lines) - (end - start)

            # Ensure a newline above each class header
            if start > 0 and md_lines[start][0:4] == '### ' and md_lines[start - 1][0:1] == '>':
                added_lines += 1
                new_lines.insert(0, '')

            md_lines[start:end] = new_lines
            return added_lines

        for key in sections:
            if key not in md_chunks:
                raise ValueError('No documentation found for %s' % key[1])
            added_lines = _replace_md(key, sections, md_chunks[key], md_lines, added_lines)

        markdown = '\n'.join(md_lines).strip() + '\n'

        if original_markdown != markdown:
            with open(md_file, 'wb') as f:
                f.write(markdown.encode('utf-8'))