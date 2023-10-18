def ctx() -> moderngl.Context:
    """ModernGL context"""
    win = window()
    if not win.ctx:
        raise RuntimeError("Attempting to get context before creation")

    return win.ctx