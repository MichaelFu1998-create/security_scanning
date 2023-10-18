def edge_label(s, edge, alpha=1.0):

    """ Visualization of the label accompanying an edge.
    """

    if s.text and edge.label != "":       
        s._ctx.nostroke()
        s._ctx.fill(
            s.text.r, 
            s.text.g, 
            s.text.b, 
            s.text.a * alpha*0.75
        )
        s._ctx.lineheight(1)    
        s._ctx.font(s.font)
        s._ctx.fontsize(s.fontsize*0.75)
        
        # Cache an outlined label text and translate it.
        # This enhances the speed and avoids wiggling text.
        try: p = edge._textpath
        except:
            try: txt = unicode(edge.label)
            except:
                try: txt = edge.label.decode("utf-8")
                except:
                    pass
            edge._textpath = s._ctx.textpath(txt, s._ctx.textwidth(" "), 0, width=s.textwidth)
            p = edge._textpath
        
        # Position the label centrally along the edge line.
        a  = degrees( atan2(edge.node2.y-edge.node1.y, edge.node2.x-edge.node1.x) )
        d  = sqrt((edge.node2.x-edge.node1.x)**2 +(edge.node2.y-edge.node1.y)**2)
        d  = abs(d-s._ctx.textwidth(edge.label)) * 0.5
        
        s._ctx.push()
        s._ctx.transform(CORNER)
        s._ctx.translate(edge.node1.x, edge.node1.y)
        s._ctx.rotate(-a)
        s._ctx.translate(d, s.fontsize*1.0)
        s._ctx.scale(alpha)
        
        # Flip labels on the left hand side so they are legible.
        if 90 < a%360 < 270:
            s._ctx.translate(s._ctx.textwidth(edge.label), -s.fontsize*2.0)
            s._ctx.transform(CENTER)
            s._ctx.rotate(180)
            s._ctx.transform(CORNER)
        
        s._ctx.drawpath(p.copy())
        s._ctx.pop()