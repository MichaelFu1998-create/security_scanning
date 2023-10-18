def _load(self, top=5, blue="blue", archive=None, member=None):
        """
        Loads a theme from aggregated web data.

        The data must be old-style Prism XML: <color>s consisting of <shade>s.
        Colors named "blue" will be overridden with the blue parameter.

        archive can be a file like object (e.g. a ZipFile)
        and will be used along with 'member' if specified.
        """
        if archive is None:
            path = os.path.join(self.cache, self.name + ".xml")
            xml = open(path).read()
        else:
            assert member is not None
            xml = archive.read(member)
        dom = parseString(xml).documentElement

        attr = lambda e, a: e.attributes[a].value

        for e in dom.getElementsByTagName("color")[:top]:
            w = float(attr(e, "weight"))
            try:
                rgb = e.getElementsByTagName("rgb")[0]
                clr = color(
                    float(attr(rgb, "r")),
                    float(attr(rgb, "g")),
                    float(attr(rgb, "b")),
                    float(attr(rgb, "a")),
                    mode="rgb"
                )
                try:
                    clr.name = attr(e, "name")
                    if clr.name == "blue": clr = color(blue)
                except:
                    pass
            except:
                name = attr(e, "name")
                if name == "blue": name = blue
                clr = color(name)

            for s in e.getElementsByTagName("shade"):
                self.ranges.append((
                    clr,
                    shade(attr(s, "name")),
                    w * float(attr(s, "weight"))
                ))