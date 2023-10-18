def _plotshare(share, names, **kwargs):
    """ make toyplot matrix fig"""

    ## set the colormap
    colormap = toyplot.color.LinearMap(toyplot.color.brewer.palette("Spectral"), 
                                 domain_min=share.min(), domain_max=share.max())

    ## set up canvas
    if not kwargs.get('width'):
        width=900
    else:
        width = kwargs['width']
    canvas = toyplot.Canvas(width=width, height=width*0.77778)

    ## order the dta
    table = canvas.matrix((share, colormap), 
                          bounds=(50, canvas.height-100,
                                  50, canvas.height-100), 
                          step=5, tshow=False, lshow=False)

    ## put a box around the table
    table.body.grid.vlines[..., [0, -1]] = 'single'
    table.body.grid.hlines[[0, -1], ...] = 'single'

    ## make hover info on grid
    for i, j in itertools.product(range(len(share)), repeat=2):
        table.body.cell(i,j).title = "%s, %s : %s" % (names[i], names[j], int(share[i,j]))

    ## create barplot
    axes = canvas.cartesian(bounds=(665, 800, 90, 560))

    ## make a hover for barplot
    zf = zip(names[::-1], share.diagonal()[::-1])
    barfloater = ["%s: %s" % (i, int(j)) for i, j in zf]

    ## plot bars
    axes.bars(share.diagonal()[::-1], along='y', title=barfloater)

    ## hide spine, move labels to the left, 
    ## use taxon names, rotate angle, align
    axes.y.spine.show = False
    axes.y.ticks.labels.offset = 0
    axes.y.ticks.locator = toyplot.locator.Explicit(range(len(names)), 
                                                    labels=names[::-1])
    axes.y.ticks.labels.angle = -90
    axes.y.ticks.labels.style = {"baseline-shift":0,
                                 "text-anchor":"end", 
                                 "font-size":"8px"}

    ## rotate xlabels, align with ticks, change to thousands, move up on canvas
    ## show ticks, and hide popup coordinates
    axes.x.ticks.labels.angle = 90
    axes.x.ticks.labels.offset = 20
    axes.x.ticks.locator = toyplot.locator.Explicit(
        range(0, int(share.max()), 
                 int(share.max() / 10)), 
        ["{}".format(i) for i in range(0, int(share.max()),
                                           int(share.max() / 10))])
    axes.x.ticks.labels.style = {"baseline-shift":0,
                                 "text-anchor":"end", 
                                 "-toyplot-anchor-shift":"15px"}
    axes.x.ticks.show = True

    ## add labels
    label_style = {"font-size": "16px", "font-weight": "bold"}
    canvas.text(300, 60, "Matrix of shared RAD loci", style=label_style)
    canvas.text(700, 60, "N RAD loci per sample", style=label_style)

    return canvas, axes