def show(self, axis=None, display=True):
        """!
        @brief Draw and show output dynamics.

        @param[in] axis (axis): If is not 'None' then user specified axis is used to display output dynamic.
        @param[in] display (bool): Whether output dynamic should be displayed or not, if not, then user
                    should call 'plt.show()' by himself.

        """
        
        if (not axis):
            (_, axis) = plt.subplots(self.__size, 1);
        
        self.__format_canvases(axis);
        
        for dynamic in self.__dynamic_storage:
            self.__display_dynamic(axis, dynamic);
        
        if (display):
            plt.show();