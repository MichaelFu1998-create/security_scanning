def html_single_plot(self,abfID,launch=False,overwrite=False):
        """create ID_plot.html of just intrinsic properties."""
        if type(abfID) is str:
            abfID=[abfID]
        for thisABFid in cm.abfSort(abfID):
            parentID=cm.parent(self.groups,thisABFid)
            saveAs=os.path.abspath("%s/%s_plot.html"%(self.folder2,parentID))
            if overwrite is False and os.path.basename(saveAs) in self.files2:
                continue
            filesByType=cm.filesByType(self.groupFiles[parentID])
            html=""
            html+='<div style="background-color: #DDDDFF;">'
            html+='<span class="title">intrinsic properties for: %s</span></br>'%parentID
            html+='<code>%s</code>'%os.path.abspath(self.folder1+"/"+parentID+".abf")
            html+='</div>'
            for fname in filesByType['plot']:
                html+=self.htmlFor(fname)
            print("creating",saveAs,'...')
            style.save(html,saveAs,launch=launch)