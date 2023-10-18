def base_boxes(self):
        """
        Get the list of vagrant base boxes
        """
        return sorted(list(set([name for name, provider in self._box_list()])))