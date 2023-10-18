def set_video_pos(self, x1, y1, x2, y2):
        """
        Set the video position on the screen

        Args:
            x1 (int): Top left x coordinate (px)
            y1 (int): Top left y coordinate (px)
            x2 (int): Bottom right x coordinate (px)
            y2 (int): Bottom right y coordinate (px)
        """
        position = "%s %s %s %s" % (str(x1),str(y1),str(x2),str(y2))
        self._player_interface.VideoPos(ObjectPath('/not/used'), String(position))