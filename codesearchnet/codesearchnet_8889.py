def _current_color(self, which=0):
        """Returns a color for the queue.

        Parameters
        ----------
        which : int (optional, default: ``0``)
            Specifies the type of color to return.

        Returns
        -------
        color : list
            Returns a RGBA color that is represented as a list with 4
            entries where each entry can be any floating point number
            between 0 and 1.

            * If ``which`` is 1 then it returns the color of the edge
              as if it were a self loop. This is specified in
              ``colors['edge_loop_color']``.
            * If ``which`` is 2 then it returns the color of the vertex
              pen color (defined as color/vertex_color in
              :meth:`.QueueNetworkDiGraph.graph_draw`). This is
              specified in ``colors['vertex_color']``.
            * If ``which`` is anything else, then it returns the a
              shade of the edge that is proportional to the number of
              agents in the system -- which includes those being
              servered and those waiting to be served. More agents
              correspond to darker edge colors. Uses
              ``colors['vertex_fill_color']`` if the queue sits on a
              loop, and ``colors['edge_color']`` otherwise.
        """
        if which == 1:
            color = self.colors['edge_loop_color']

        elif which == 2:
            color = self.colors['vertex_color']

        else:
            div = self.coloring_sensitivity * self.num_servers + 1.
            tmp = 1. - min(self.num_system / div, 1)

            if self.edge[0] == self.edge[1]:
                color = [i * tmp for i in self.colors['vertex_fill_color']]
                color[3] = 1.0
            else:
                color = [i * tmp for i in self.colors['edge_color']]
                color[3] = 1 / 2.

        return color