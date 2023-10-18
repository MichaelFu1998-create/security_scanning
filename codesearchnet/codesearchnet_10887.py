def eval(self, x, y, z):
        """Evaluate the function in (x, y, z)."""
        xc, yc, zc = self.rc
        sx, sy, sz = self.s

        ## Method1: direct evaluation
        #return exp(-(((x-xc)**2)/(2*sx**2) + ((y-yc)**2)/(2*sy**2) +\
        #        ((z-zc)**2)/(2*sz**2)))

        ## Method2: evaluation using numexpr
        def arg(s):
            return "((%s-%sc)**2)/(2*s%s**2)" % (s, s, s)
        return NE.evaluate("exp(-(%s + %s + %s))" %
                           (arg("x"), arg("y"), arg("z")))