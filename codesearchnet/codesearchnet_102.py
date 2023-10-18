def generate_similar_points_manhattan(self, nb_steps, step_size, return_array=False):
        """
        Generate nearby points to this keypoint based on manhattan distance.

        To generate the first neighbouring points, a distance of S (step size) is moved from the
        center point (this keypoint) to the top, right, bottom and left, resulting in four new
        points. From these new points, the pattern is repeated. Overlapping points are ignored.

        The resulting points have a shape similar to a square rotated by 45 degrees.

        Parameters
        ----------
        nb_steps : int
            The number of steps to move from the center point. nb_steps=1 results in a total of
            5 output points (1 center point + 4 neighbours).

        step_size : number
            The step size to move from every point to its neighbours.

        return_array : bool, optional
            Whether to return the generated points as a list of keypoints or an array
            of shape ``(N,2)``, where ``N`` is the number of generated points and the second axis contains
            the x- (first value) and y- (second value) coordinates.

        Returns
        -------
        points : list of imgaug.Keypoint or (N,2) ndarray
            If return_array was False, then a list of Keypoint.
            Otherwise a numpy array of shape ``(N,2)``, where ``N`` is the number of generated points and
            the second axis contains the x- (first value) and y- (second value) coordinates.
            The center keypoint (the one on which this function was called) is always included.

        """
        # TODO add test
        # Points generates in manhattan style with S steps have a shape similar to a 45deg rotated
        # square. The center line with the origin point has S+1+S = 1+2*S points (S to the left,
        # S to the right). The lines above contain (S+1+S)-2 + (S+1+S)-2-2 + ... + 1 points. E.g.
        # for S=2 it would be 3+1=4 and for S=3 it would be 5+3+1=9. Same for the lines below the
        # center. Hence the total number of points is S+1+S + 2*(S^2).
        points = np.zeros((nb_steps + 1 + nb_steps + 2*(nb_steps**2), 2), dtype=np.float32)

        # we start at the bottom-most line and move towards the top-most line
        yy = np.linspace(self.y - nb_steps * step_size, self.y + nb_steps * step_size, nb_steps + 1 + nb_steps)

        # bottom-most line contains only one point
        width = 1

        nth_point = 0
        for i_y, y in enumerate(yy):
            if width == 1:
                xx = [self.x]
            else:
                xx = np.linspace(self.x - (width-1)//2 * step_size, self.x + (width-1)//2 * step_size, width)
            for x in xx:
                points[nth_point] = [x, y]
                nth_point += 1
            if i_y < nb_steps:
                width += 2
            else:
                width -= 2

        if return_array:
            return points
        return [self.deepcopy(x=points[i, 0], y=points[i, 1]) for i in sm.xrange(points.shape[0])]