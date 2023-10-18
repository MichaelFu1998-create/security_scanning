def ellipse(self, org_x, org_y, radius_x, radius_y, arc_start, arc_end):
        """
        :param org_x: origination x axis
        :param org_y: origination y axis
        :param radius_x: radius x axis
        :param radius_y: radius y axis
        :param arc_start: arc start angle
        :param arc_end: arc end angle
        """
        ellipse = pgmagick.DrawableEllipse(float(org_x), float(org_y),
                                           float(radius_x), float(radius_y),
                                           float(arc_start), float(arc_end))
        self.drawer.append(ellipse)