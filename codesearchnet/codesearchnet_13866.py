def node_label(s, node, alpha=1.0):

    """ Visualization of a node's id.
    """

    if s.text:
        #s._ctx.lineheight(1)    
        s._ctx.font(s.font)
        s._ctx.fontsize(s.fontsize)
        s._ctx.nostroke()
        s._ctx.fill(
            s.text.r, 
            s.text.g, 
            s.text.b, 
            s.text.a * alpha
        )

        # Cache an outlined label text and translate it.
        # This enhances the speed and avoids wiggling text.
        try: p = node._textpath
        except: 
            txt = node.label
            try: txt = unicode(txt)
            except:
                try: txt = txt.decode("utf-8")
                except:
                    pass
            # Abbreviation.
            #root = node.graph.root
            #if txt != root and txt[-len(root):] == root: 
            #    txt = txt[:len(txt)-len(root)]+root[0]+"."
            dx, dy = 0, 0
            if s.align == 2: #CENTER
                dx = -s._ctx.textwidth(txt, s.textwidth) / 2
                dy =  s._ctx.textheight(txt) / 2
            node._textpath = s._ctx.textpath(txt, dx, dy, width=s.textwidth)
            p = node._textpath
        
        if s.depth:
            try: __colors.shadow(dx=2, dy=4, blur=5, alpha=0.3*alpha)
            except: pass
        
        s._ctx.push()
        s._ctx.translate(node.x, node.y)
        s._ctx.scale(alpha)
        s._ctx.drawpath(p.copy())
        s._ctx.pop()