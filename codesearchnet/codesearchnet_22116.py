def tile():
    """Tiles open figures."""

    figs = plt.get_fignums()

    # Keep track of x, y, size for figures
    x       = 0
    y       = 0
    # maxy    = 0
    toppad  = 21

    size = np.array([0, 0])

    if ( len(figs) != 0 ):
        fig     = plt.figure(figs[0])
        screen  = fig.canvas.window.get_screen()
        screenx = screen.get_monitor_geometry(screen.get_primary_monitor())
        screenx = screenx[2]
    
        fig = plt.figure(figs[0])
        fig.canvas.manager.window.move(x, y)
        maxy = np.array(fig.canvas.manager.window.get_position())[1]
        size = np.array(fig.canvas.manager.window.get_size())
        y    = maxy
        x += size[0]+1
    
        for fig in figs[1:]:
            fig  = plt.figure(fig)
            size = np.array(fig.canvas.manager.window.get_size())
            if ( x+size[0] > screenx ):
                x    = 0
                y    = maxy
                maxy = y+size[1]+toppad
            else:
                maxy = max(maxy, y+size[1]+toppad)
            fig.canvas.manager.window.move(x, y)
            x += size[0] + 1