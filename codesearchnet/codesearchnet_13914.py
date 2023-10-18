def textmetrics(self, txt, width=None, height=None, **kwargs):
        '''Returns the width and height of a string of text as a tuple
        (according to current font settings).
        '''
        # for now only returns width and height (as per Nodebox behaviour)
        # but maybe we could use the other data from cairo
        
        # we send doRender=False to prevent the actual rendering process, only the path generation is enabled
        # not the most efficient way, but it generates accurate results
        txt = self.Text(txt, 0, 0, width, height, enableRendering=False, **kwargs)
        return txt.metrics