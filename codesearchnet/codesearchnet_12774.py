def adjust_angles(self, start_node, start_angle, end_node, end_angle):
        """
        This function adjusts the start and end angles to correct for
        duplicated axes.
        """
        start_group = self.find_node_group_membership(start_node)
        end_group = self.find_node_group_membership(end_node)

        if start_group == 0 and end_group == len(self.nodes.keys())-1:
            if self.has_edge_within_group(start_group):
                start_angle = correct_negative_angle(start_angle -
                                                     self.minor_angle)
            if self.has_edge_within_group(end_group):
                end_angle = correct_negative_angle(end_angle +
                                                   self.minor_angle)

        elif start_group == len(self.nodes.keys())-1 and end_group == 0:
            if self.has_edge_within_group(start_group):
                start_angle = correct_negative_angle(start_angle +
                                                     self.minor_angle)
            if self.has_edge_within_group(end_group):
                end_angle = correct_negative_angle(end_angle -
                                                   self.minor_angle)

        elif start_group < end_group:
            if self.has_edge_within_group(end_group):
                end_angle = correct_negative_angle(end_angle -
                                                   self.minor_angle)
            if self.has_edge_within_group(start_group):
                start_angle = correct_negative_angle(start_angle +
                                                     self.minor_angle)

        elif end_group < start_group:
            if self.has_edge_within_group(start_group):
                start_angle = correct_negative_angle(start_angle -
                                                     self.minor_angle)
            if self.has_edge_within_group(end_group):
                end_angle = correct_negative_angle(end_angle +
                                                   self.minor_angle)

        return start_angle, end_angle