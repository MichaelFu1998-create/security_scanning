def things_near(self, location, radius=None):
        "Return all things within radius of location."
        if radius is None: radius = self.perceptible_distance
        radius2 = radius * radius
        return [thing for thing in self.things
                if distance2(location, thing.location) <= radius2]