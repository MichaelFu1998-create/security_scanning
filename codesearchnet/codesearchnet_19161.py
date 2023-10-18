def filter(self):
        """Filter the changesets that intersects with the geojson geometry."""
        self.content = [
            ch
            for ch in self.xml.getchildren()
            if get_bounds(ch).intersects(self.area)
            ]