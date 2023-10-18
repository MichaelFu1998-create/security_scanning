def draw_list(markup, x, y, w, padding=5, callback=None):
    
    """ Draws list markup with indentation in NodeBox.

    Draw list markup at x, y coordinates
    using indented bullets or numbers.
    The callback is a command that takes a str and an int.
    
    """
    
    try: from web import _ctx
    except: pass

    i = 1
    for chunk in markup.split("\n"):
        
        if callback != None: 
            callback(chunk, i)
        
        m = re.search("^([0-9]{1,3}\. )", chunk.lstrip())
        if m:
            indent = re.search("[0-9]", chunk).start()*padding*2
            bullet = m.group(1)
            dx = textwidth("000.")
            chunk = chunk.lstrip(m.group(1)+"\t")
        
        if chunk.lstrip().startswith("*"):
            indent = chunk.find("*")*padding*2
            bullet = u"•"
            dx = textwidth("*")
            chunk = chunk.lstrip("* \t")
        
        _ctx.text(bullet, x+indent, y)
        dx += padding + indent
        _ctx.text(chunk, x+dx, y, width=w-dx)
        y += _ctx.textheight(chunk, width=w-dx)
        y += _ctx.textheight(" ") * 0.25
        i += 1