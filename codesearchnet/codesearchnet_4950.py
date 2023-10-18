def append_dynamics(self, t, dynamics, canvas=0, separate=False, color='blue'):
        """!
        @brief Append several dynamics to canvas or canvases (defined by 'canvas' and 'separate' arguments).

        @param[in] t (list): Time points that corresponds to dynamic values and considered on a X axis.
        @param[in] dynamics (list): Dynamics where each of them is considered on Y axis.
        @param[in] canvas (uint): Index of canvas where dynamic should be displayed, in case of 'separate'
                    representation this argument is considered as a first canvas from that displaying should be done.
        @param[in] separate (bool|list): If 'True' then each dynamic is displayed on separate canvas, if it is defined
                    by list, for example, [ [1, 2], [3, 4] ], then the first and the second dynamics are displayed on
                    the canvas with index 'canvas' and the third and forth are displayed on the next 'canvas + 1'
                    canvas.
        @param[in] color (string): Color that is used to display output dynamic(s).

        """
        description = dynamic_descr(canvas, t, dynamics, separate, color);
        self.__dynamic_storage.append(description);
        self.__update_canvas_xlim(description.time, description.separate);