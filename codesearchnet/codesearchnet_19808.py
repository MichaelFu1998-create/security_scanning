def comments_load(self):
        """read the header and populate self with information about comments"""
        self.comment_times,self.comment_sweeps,self.comment_tags=[],[],[]
        self.comments=0 # will be >0 if comments exist
        self.comment_text=""

        try:
            # this used to work
            self.comment_tags = list(self.ABFblock.segments[0].eventarrays[0].annotations['comments'])
            self.comment_times = list(self.ABFblock.segments[0].eventarrays[0].times/self.trace.itemsize)
            self.comment_sweeps = list(self.comment_times)
        except:
            # now this notation seems to work
            for events in self.ABFblock.segments[0].events: # this should only happen once actually
                self.comment_tags = events.annotations['comments'].tolist()
                self.comment_times = np.array(events.times.magnitude/self.trace.itemsize)
                self.comment_sweeps = self.comment_times/self.sweepInterval

        for i,c in enumerate(self.comment_tags):
            self.comment_tags[i]=c.decode("utf-8")