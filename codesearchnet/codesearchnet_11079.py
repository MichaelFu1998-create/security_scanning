def draw(self, time, frametime, target):
        """
        Fetch track value for every runnable effect.
        If the value is > 0.5 we draw it.
        """
        for effect in self.effects:
            value = effect.rocket_timeline_track.time_value(time)
            if value > 0.5:
                effect.draw(time, frametime, target)