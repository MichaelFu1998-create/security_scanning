def contig_coords(self):
        '''Finds coords of contigs, i.e. everything that's not a gap (N or n). Returns a list of Intervals. Coords are zero-based'''
        # contigs are the opposite of gaps, so work out the coords from the gap coords
        gaps = self.gaps()

        if len(gaps) == 0:
            return [intervals.Interval(0, len(self) - 1)]

        coords = [0]
        for g in gaps:
            if g.start == 0:
                coords = [g.end + 1]
            else:
                coords += [g.start - 1, g.end + 1]

        if coords[-1] < len(self):
            coords.append(len(self) - 1)

        return [intervals.Interval(coords[i], coords[i+1]) for i in range(0, len(coords)-1,2)]