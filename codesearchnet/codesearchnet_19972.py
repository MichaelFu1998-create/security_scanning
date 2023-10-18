def generate_colormap(self,colormap=None,reverse=False):
        """use 1 colormap for the whole abf. You can change it!."""
        if colormap is None:
            colormap = pylab.cm.Dark2
        self.cm=colormap
        self.colormap=[]
        for i in range(self.sweeps): #TODO: make this the only colormap
            self.colormap.append(colormap(i/self.sweeps))
        if reverse:
            self.colormap.reverse()