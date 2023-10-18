def figure(self,forceNew=False):
        """make sure a figure is ready."""
        if plt._pylab_helpers.Gcf.get_num_fig_managers()>0 and forceNew is False:
            self.log.debug("figure already seen, not creating one.")
            return

        if self.subplot:
            self.log.debug("subplot mode enabled, not creating new figure")
        else:
            self.log.debug("creating new figure")
            plt.figure(figsize=(self.figure_width,self.figure_height))