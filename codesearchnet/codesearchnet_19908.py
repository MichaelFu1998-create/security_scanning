def comments(self,minutes=False):
        """
        Add comment lines/text to an existing plot. Defaults to seconds.
        Call after a plot has been made, and after margins have been set.
        """
        if self.comments==0:
            return
        self.log.debug("adding comments to plot")
        for i,t in enumerate(self.abf.comment_times):
            if minutes:
                t/=60.0
            plt.axvline(t,color='r',ls=':')
            X1,X2,Y1,Y2=plt.axis()
            Y2=Y2-abs(Y2-Y1)*.02
            plt.text(t,Y2,self.abf.comment_tags[i],color='r',rotation='vertical',
                     ha='right',va='top',weight='bold',alpha=.5,size=8,)