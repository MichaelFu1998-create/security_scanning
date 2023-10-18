def render(self, size, frame, drawqueue):
        '''
        Calls implmentation to get a render context,
        passes it to the drawqueues render function
        then calls self.rendering_finished
        '''
        r_context = self.create_rcontext(size, frame)
        drawqueue.render(r_context)
        self.rendering_finished(size, frame, r_context)
        return r_context