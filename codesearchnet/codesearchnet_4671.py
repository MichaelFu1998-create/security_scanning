def set_canvas_title(self, text, canvas = 0):
        """!
        @brief Set title for specified canvas.
        
        @param[in] text (string): Title for canvas.
        @param[in] canvas (uint): Index of canvas where title should be displayed.
        
        """
        
        if canvas > self.__number_canvases:
            raise NameError('Canvas does ' + canvas + ' not exists.')
        
        self.__canvas_titles[canvas] = text