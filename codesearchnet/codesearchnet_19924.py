def html_index(self,launch=False,showChildren=False):
        """
        generate list of cells with links. keep this simple.
        automatically generates splash page and regnerates frames.
        """
        self.makePics() # ensure all pics are converted
        # generate menu
        html='<a href="index_splash.html" target="content">./%s/</a><br>'%os.path.basename(self.abfFolder)
        for ID in smartSort(self.fnamesByCell.keys()):
            link=''
            if ID+".html" in self.fnames2:
                link='href="%s.html" target="content"'%ID
            html+=('<a %s>%s</a><br>'%(link,ID)) # show the parent ABF (ID)
            if showChildren:
                for fname in self.fnamesByCell[ID]:
                    thisID=os.path.splitext(fname)[0]
                    files2=[x for x in self.fnames2 if x.startswith(thisID) and not x.endswith(".html")]
                    html+='<i>%s</i>'%thisID # show the child ABF
                    if len(files2):
                        html+=' (%s)'%len(files2) # show number of supporting files
                    html+='<br>'
                html+="<br>"
        style.save(html,self.abfFolder2+"/index_menu.html")
        self.html_index_splash() # make splash page
        style.frames(self.abfFolder2+"/index.html",launch=launch)