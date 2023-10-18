def __create_surface(self, dimension):
        """!
        @brief Prepares surface for showing network structure in line with specified dimension.
        
        @param[in] dimension (uint): Dimension of processed data (external stimulus).
        
        @return (tuple) Description of surface for drawing network structure.
        
        """
        
        rcParams['font.sans-serif'] = ['Arial']
        rcParams['font.size'] = 12

        fig = plt.figure()
        axes = None
        if dimension == 2:
            axes = fig.add_subplot(111)
        elif dimension == 3:
            axes = fig.gca(projection='3d')
        
        surface_font = FontProperties()
        surface_font.set_name('Arial')
        surface_font.set_size('12')
        
        return (fig, axes)