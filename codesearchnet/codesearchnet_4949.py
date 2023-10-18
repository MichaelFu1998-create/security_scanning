def append_dynamic(self, t, dynamic, canvas=0, color='blue'):
        """!
        @brief Append single dynamic to specified canvas (by default to the first with index '0').

        @param[in] t (list): Time points that corresponds to dynamic values and considered on a X axis.
        @param[in] dynamic (list): Value points of dynamic that are considered on an Y axis.
        @param[in] canvas (uint): Canvas where dynamic should be displayed.
        @param[in] color (string): Color that is used for drawing dynamic on the canvas.

        """
        description = dynamic_descr(canvas, t, dynamic, False, color);
        self.__dynamic_storage.append(description);
        self.__update_canvas_xlim(description.time, description.separate);