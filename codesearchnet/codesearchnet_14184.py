def draw_table(table, x, y, w, padding=5):
    
    """ This is a very poor algorithm to draw Wikipedia tables in NodeBox.
    """
    
    try: from web import _ctx
    except: pass
    
    f = _ctx.fill()
    _ctx.stroke(f)
    h = _ctx.textheight(" ") + padding*2
    
    row_y = y
    
    if table.title != "":
        _ctx.fill(f)
        _ctx.rect(x, row_y, w, h)
        _ctx.fill(1)
        _ctx.text(table.title, x+padding, row_y+_ctx.fontsize()+ padding)
        row_y += h
    
    # A table of flags marking how long a cell 
    # from a previous row is still spanning in a column.
    rowspans = [1 for i in range(10)]
    previous_cell_w = 0
    
    for row in table:
        
        cell_x = x
        
        # The width of a cell is the total table width 
        # evenly divided by the number of cells.
        # Previous rows' cells still spanning will push cells
        # to the right and decrease their width.
        cell_w  = 1.0 * w
        cell_w -= previous_cell_w * len([n for n in rowspans if n > 1])
        cell_w /= len(row)
        
        # The height of each cell is the highest cell in the row.
        # The height depends on the amount of text in the cell.
        cell_h = 0
        for cell in row:
            this_h = _ctx.textheight(cell, width=cell_w-padding*2) + padding*2
            cell_h = max(cell_h, this_h)
        
        # Traverse each cell in this row.
        i = 0
        for cell in row:
            
            # If a previous row's cell is still spanning,
            # push this cell to the right.
            if rowspans[i] > 1:
                rowspans[i] -= 1
                cell_x += previous_cell_w
                i += 1
                
            # Get the rowspan attribute for this cell.
            m = re.search("rowspan=\"(.*?)\"", cell.properties)
            if m:
                rowspan = int(m.group(1))
                rowspans[i] = rowspan
            else:
                rowspan = 1

            # Padded cell text.            
            # Horizontal line above each cell.
            # Vertical line before each cell.
            _ctx.fill(f)
            _ctx.text(cell, cell_x+padding, row_y+_ctx.fontsize()+padding, cell_w-padding*2)
            _ctx.line(cell_x, row_y, cell_x+cell_w, row_y)
            if cell_x > x:
                _ctx.nofill()
                _ctx.line(cell_x, row_y, cell_x, row_y+cell_h)
                
            cell_x += cell_w
            i += 1
            
        # Move to next row.
        row_y += cell_h
        previous_cell_w = cell_w
        
    # Table's bounding rectangle.
    _ctx.nofill()
    _ctx.rect(x, y, w, row_y-y)