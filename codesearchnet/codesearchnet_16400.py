def get_2d_markers(
        self, component_info=None, data=None, component_position=None, index=None
    ):
        """Get 2D markers.

        :param index: Specify which camera to get 2D from, will be returned as
                      first entry in the returned array.
        """
        return self._get_2d_markers(
            data, component_info, component_position, index=index
        )