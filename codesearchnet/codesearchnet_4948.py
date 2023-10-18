def set_canvas_properties(self, canvas, x_title=None, y_title=None, x_lim=None, y_lim=None, x_labels=True, y_labels=True):
        """!
        @brief Set properties for specified canvas.

        @param[in] canvas (uint): Index of canvas whose properties should changed.
        @param[in] x_title (string): Title for X axis, if 'None', then nothing is displayed.
        @param[in] y_title (string): Title for Y axis, if 'None', then nothing is displayed.
        @param[in] x_lim (list): Defines borders of X axis like [from, to], for example [0, 3.14], if 'None' then
                    borders are calculated automatically.
        @param[in] y_lim (list): Defines borders of Y axis like [from, to], if 'None' then borders are calculated
                    automatically.
        @param[in] x_labels (bool): If True then labels of X axis are displayed.
        @param[in] y_labels (bool): If True then labels of Y axis are displayed.

        """
        self.__canvases[canvas] = canvas_descr(x_title, y_title, x_lim, y_lim, x_labels, y_labels);