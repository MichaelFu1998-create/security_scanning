def video_pos(self):
        """
        Returns:
            (int, int, int, int): Video spatial position (x1, y1, x2, y2) where (x1, y1) is top left,
                                  and (x2, y2) is bottom right. All values in px.
        """
        position_string = self._player_interface.VideoPos(ObjectPath('/not/used'))
        return list(map(int, position_string.split(" ")))