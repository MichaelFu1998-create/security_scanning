def walk_ast(node, code_lines, sections, md_chunks):
    """
    A callback used to walk the Python AST looking for classes, functions,
    methods and attributes. Generates chunks of markdown markup to replace
    the existing content.

    :param node:
        An _ast module node object

    :param code_lines:
        A list of unicode strings - the source lines of the Python file

    :param sections:
        A dict of markdown document sections that need to be updated. The key
        will be a two-element tuple of the section type ("class", "function",
        "method" or "attribute") and identifier. The values are a two-element
        tuple of the start and end line number in the markdown document of the
        section.

    :param md_chunks:
        A dict with keys from the sections param and the values being a unicode
        string containing a chunk of markdown markup.
    """

    if isinstance(node, _ast.FunctionDef):
        key = ('function', node.name)
        if key not in sections:
            return

        docstring = ast.get_docstring(node)
        def_lineno = node.lineno + len(node.decorator_list)

        definition, description_md = _get_func_info(docstring, def_lineno, code_lines, '> ')

        md_chunk = textwrap.dedent("""
            ### `%s()` function

            > ```python
            > %s
            > ```
            >
            %s
        """).strip() % (
            node.name,
            definition,
            description_md
        ) + "\n"

        md_chunks[key] = md_chunk.replace('>\n\n', '')

    elif isinstance(node, _ast.ClassDef):
        if ('class', node.name) not in sections:
            return

        for subnode in node.body:
            if isinstance(subnode, _ast.FunctionDef):
                node_id = node.name + '.' + subnode.name

                method_key = ('method', node_id)
                is_method = method_key in sections

                attribute_key = ('attribute', node_id)
                is_attribute = attribute_key in sections

                is_constructor = subnode.name == '__init__'

                if not is_constructor and not is_attribute and not is_method:
                    continue

                docstring = ast.get_docstring(subnode)
                def_lineno = subnode.lineno + len(subnode.decorator_list)

                if not docstring:
                    continue

                if is_method or is_constructor:
                    definition, description_md = _get_func_info(docstring, def_lineno, code_lines, '> > ')

                    if is_constructor:
                        key = ('class', node.name)

                        class_docstring = ast.get_docstring(node) or ''
                        class_description = textwrap.dedent(class_docstring).strip()
                        if class_description:
                            class_description_md = "> %s\n>" % (class_description.replace("\n", "\n> "))
                        else:
                            class_description_md = ''

                        md_chunk = textwrap.dedent("""
                            ### `%s()` class

                            %s
                            > ##### constructor
                            >
                            > > ```python
                            > > %s
                            > > ```
                            > >
                            %s
                        """).strip() % (
                            node.name,
                            class_description_md,
                            definition,
                            description_md
                        )

                        md_chunk = md_chunk.replace('\n\n\n', '\n\n')

                    else:
                        key = method_key

                        md_chunk = textwrap.dedent("""
                            >
                            > ##### `.%s()` method
                            >
                            > > ```python
                            > > %s
                            > > ```
                            > >
                            %s
                        """).strip() % (
                            subnode.name,
                            definition,
                            description_md
                        )

                    if md_chunk[-5:] == '\n> >\n':
                        md_chunk = md_chunk[0:-5]

                else:
                    key = attribute_key

                    description = textwrap.dedent(docstring).strip()
                    description_md = "> > %s" % (description.replace("\n", "\n> > "))

                    md_chunk = textwrap.dedent("""
                        >
                        > ##### `.%s` attribute
                        >
                        %s
                    """).strip() % (
                        subnode.name,
                        description_md
                    )

                md_chunks[key] = re.sub('[ \\t]+\n', '\n', md_chunk.rstrip())

    elif isinstance(node, _ast.If):
        for subast in node.body:
            walk_ast(subast, code_lines, sections, md_chunks)
        for subast in node.orelse:
            walk_ast(subast, code_lines, sections, md_chunks)