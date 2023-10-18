def adapt_animation_layout(animation):
    """
    Adapt the setter in an animation's layout so that Strip animations can run
    on on Matrix, Cube, or Circle layout, and Matrix or Cube animations can run
    on a Strip layout.
    """
    layout = animation.layout
    required = getattr(animation, 'LAYOUT_CLASS', None)

    if not required or isinstance(layout, required):
        return

    msg = LAYOUT_WARNING % (
        type(animation).__name__, required.__name__, type(layout).__name__)

    setter = layout.set
    adaptor = None

    if required is strip.Strip:
        if isinstance(layout, matrix.Matrix):
            width = layout.width

            def adaptor(pixel, color=None):
                y, x = divmod(pixel, width)
                setter(x, y, color or BLACK)

        elif isinstance(layout, cube.Cube):
            lx, ly = layout.x, layout.y

            def adaptor(pixel, color=None):
                yz, x = divmod(pixel, lx)
                z, y = divmod(yz, ly)
                setter(x, y, z, color or BLACK)

        elif isinstance(layout, circle.Circle):

            def adaptor(pixel, color=None):
                layout._set_base(pixel, color or BLACK)

    elif required is matrix.Matrix:
        if isinstance(layout, strip.Strip):
            width = animation.width

            def adaptor(x, y, color=None):
                setter(x + y * width, color or BLACK)

    if not adaptor:
        raise ValueError(msg)

    log.warning(msg)
    animation.layout.set = adaptor