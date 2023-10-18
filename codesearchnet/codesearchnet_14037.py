def export_svg(self):
        
        """ Exports the path as SVG.
        
        Uses the filename given when creating this object.
        The file is automatically updated to reflect
        changes to the path.
        
        """
        
        d = ""
        if len(self._points) > 0:
            d += "M "+str(self._points[0].x)+" "+str(self._points[0].y)+" "
            for pt in self._points:
                if pt.cmd == MOVETO:
                    d += "M "+str(pt.x)+" "+str(pt.y)+" "
                elif pt.cmd == LINETO:
                    d += "L "+str(pt.x)+" "+str(pt.y)+" "
                elif pt.cmd == CURVETO:
                    d += "C "
                    d += str(pt.ctrl1.x)+" "+str(pt.ctrl1.y)+" "
                    d += str(pt.ctrl2.x)+" "+str(pt.ctrl2.y)+" "
                    d += str(pt.x)+" "+str(pt.y)+" "
        
        c = "rgb("
        c += str(int(self.path_color.r*255)) + ","
        c += str(int(self.path_color.g*255)) + ","
        c += str(int(self.path_color.b*255)) + ")"
        
        s  = '<?xml version="1.0"?>\n'
        s += '<svg width="'+str(_ctx.WIDTH)+'pt" height="'+str(_ctx.HEIGHT)+'pt">\n'
        s += '<g>\n'
        s += '<path d="'+d+'" fill="none" stroke="'+c+'" stroke-width="'+str(self.strokewidth)+'" />\n'
        s += '</g>\n'
        s += '</svg>\n'
        
        f = open(self.file+".svg", "w")
        f.write(s)
        f.close()