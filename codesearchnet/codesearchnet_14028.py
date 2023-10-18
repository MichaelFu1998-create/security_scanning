def overlap(self, x1, y1, x2, y2, r=5):
        
        """ Returns True when point 1 and point 2 overlap.
        
        There is an r treshold in which point 1 and point 2
        are considered to overlap.
        
        """
        
        if abs(x2-x1) < r and abs(y2-y1) < r:
            return True
        else:
            return False