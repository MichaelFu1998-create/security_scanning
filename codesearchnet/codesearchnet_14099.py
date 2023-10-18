def swarm(self, x, y, r=100):
        """
        Fancy random ovals for all the colors in the list.
        """
        sc = _ctx.stroke(0, 0, 0, 0)
        sw = _ctx.strokewidth(0)

        _ctx.push()
        _ctx.transform(_ctx.CORNER)
        _ctx.translate(x, y)

        for i in _range(r * 3):
            clr = choice(self).copy()
            clr.alpha -= 0.5 * random()
            _ctx.fill(clr)
            clr = choice(self)
            _ctx.stroke(clr)
            _ctx.strokewidth(10 * random())

            _ctx.rotate(360 * random())

            r2 = r * 0.5 * random()
            _ctx.oval(r * random(), 0, r2, r2)
        _ctx.pop()

        _ctx.strokewidth(sw)
        if sc is None:
            _ctx.nostroke()
        else:
            _ctx.stroke(sc)