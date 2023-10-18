def get_class_traits(klass):
    """ Yield all of the documentation for trait definitions on a class object.
    """
    # FIXME: gracefully handle errors here or in the caller?
    source = inspect.getsource(klass)
    cb = CommentBlocker()
    cb.process_file(StringIO(source))
    mod_ast = compiler.parse(source)
    class_ast = mod_ast.node.nodes[0]
    for node in class_ast.code.nodes:
        # FIXME: handle other kinds of assignments?
        if isinstance(node, compiler.ast.Assign):
            name = node.nodes[0].name
            rhs = unparse(node.expr).strip()
            doc = strip_comment_marker(cb.search_for_comment(node.lineno, default=''))
            yield name, rhs, doc