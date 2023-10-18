def get_modeltree(model=None):
    """Alias to :func:`get_tree`."""
    if model is None:
        model = mx.cur_model()
    treemodel = ModelTreeModel(model._baseattrs)
    view = QTreeView()
    view.setModel(treemodel)
    view.setWindowTitle("Model %s" % model.name)
    view.setAlternatingRowColors(True)
    return view