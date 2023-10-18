def text_decoration(self, decoration):
        """text decoration

        :param decoration: 'no', 'underline', 'overline', 'linethrough'
        :type decoration: str
        """
        if decoration.lower() == 'linethrough':
            d = pgmagick.DecorationType.LineThroughDecoration
        else:
            decoration_type_string = "%sDecoration" % decoration.title()
            d = getattr(pgmagick.DecorationType, "%s" % decoration_type_string)
        decoration = pgmagick.DrawableTextDecoration(d)
        self.drawer.append(decoration)