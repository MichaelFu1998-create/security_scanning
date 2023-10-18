def show_tree(model=None):
    """Display the model tree window.

    Args:
        model: :class:`Model <modelx.core.model.Model>` object.
            Defaults to the current model.

    Warnings:
        For this function to work with Spyder, *Graphics backend* option
        of Spyder must be set to *inline*.
    """
    if model is None:
        model = mx.cur_model()
    view = get_modeltree(model)
    app = QApplication.instance()
    if not app:
        raise RuntimeError("QApplication does not exist.")
    view.show()
    app.exec_()