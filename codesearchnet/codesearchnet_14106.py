def _xml(self):
        """
        Returns the color information as XML.

        The XML has the following structure:
        <colors query="">
            <color name="" weight="" />
                <rgb r="" g="" b="" />
                <shade name="" weight="" />
            </color>
        </colors>

        Notice that ranges are stored by name and retrieved in the _load()
        method with the shade() command - and are thus expected to be
        shades (e.g. intense, warm, ...) unless the shade() command would
        return any custom ranges as well. This can be done by appending custom
        ranges to the shades list.
        """
        grouped = self._weight_by_hue()

        xml = "<colors query=\"" + self.name + "\" tags=\"" + ", ".join(self.tags) + "\">\n\n"
        for total_weight, normalized_weight, hue, ranges in grouped:
            if hue == self.blue: hue = "blue"
            clr = color(hue)
            xml += "\t<color name=\"" + clr.name + "\" weight=\"" + str(normalized_weight) + "\">\n "
            xml += "\t\t<rgb r=\"" + str(clr.r) + "\" g=\"" + str(clr.g) + "\" "
            xml += "b=\"" + str(clr.b) + "\" a=\"" + str(clr.a) + "\" />\n "
            for clr, rng, wgt in ranges:
                xml += "\t\t<shade name=\"" + str(rng) + "\" weight=\"" + str(wgt / total_weight) + "\" />\n "
            xml = xml.rstrip(" ") + "\t</color>\n\n"
        xml += "</colors>"

        return xml