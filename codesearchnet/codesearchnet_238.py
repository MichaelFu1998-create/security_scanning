def get_intersections_with_segments(self):
        """
        Return a list of unordered intersection '(point, segment)' pairs,
        where segments may contain 2 or more values.
        """
        if Real is float:
            return [
                (p, [event.segment for event in event_set])
                for p, event_set in self.intersections.items()
            ]
        else:
            return [
                (
                    (float(p[0]), float(p[1])),
                    [((float(event.segment[0][0]), float(event.segment[0][1])),
                      (float(event.segment[1][0]), float(event.segment[1][1])))
                     for event in event_set],
                )
                for p, event_set in self.intersections.items()
            ]