def reset_colors(self):
        """Resets all edge and vertex colors to their default values."""
        for k, e in enumerate(self.g.edges()):
            self.g.set_ep(e, 'edge_color', self.edge2queue[k].colors['edge_color'])
        for v in self.g.nodes():
            self.g.set_vp(v, 'vertex_fill_color', self.colors['vertex_fill_color'])